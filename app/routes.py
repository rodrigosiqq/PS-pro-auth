import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from .models import User
from .database import db
from functools import wraps

# O nome aqui DEVE ser auth_bp para coincidir com o __init__.py
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username e password sao obrigatorios"}), 400

    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"error": "Usuario ja existe"}), 400
        
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
        # Gerando o Token JWT
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            "token": token,
            "user": user.to_dict()
        }), 200
        
    return jsonify({"error": "Credenciais invalidas"}), 401

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
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token invalido!'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_user_data(current_user):
    return jsonify(current_user.to_dict()), 200