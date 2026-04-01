import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from .models import User  # Certifique-se que o modelo se chama User
from .database import db
from functools import wraps

# Mantendo o nome auth_bp para coincidir com seu __init__
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token and 'Bearer ' in token:
            token = token.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token faltando!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            # Buscando o objeto completo do usuário
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Usuário não encontrado!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token invalido!', 'details': str(e)}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username e password sao obrigatorios"}), 400

    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"error": "Usuario ja existe"}), 400
        
    # Adicionando username e cargo (ajuste os campos conforme seu models.py)
    new_user = User(username=data.get('username'), cargo=data.get('cargo', 'tecnico'))
    new_user.set_password(data.get('password'))
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuario criado com sucesso!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and user.check_password(data.get('password')):
        token = jwt.encode({
            'user_id': user.id,
            'nome': user.username, # Incluindo o nome no token para o Front-end ler
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            "token": token,
            "user": user.to_dict()
        }), 200
        
    return jsonify({"error": "Credenciais invalidas"}), 401

# CORRIGIDO: Usando auth_bp e User.query
@auth_bp.route('/usuarios', methods=['GET'])
@token_required
def listar_usuarios(current_user):
    # Retorna todos os usuários para o Select do técnico entrante
    usuarios = User.query.all()
    return jsonify([{"id": u.id, "nome": u.username} for u in usuarios]), 200

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_user_data(current_user):
    return jsonify(current_user.to_dict()), 200