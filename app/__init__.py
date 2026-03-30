import os
from flask import Flask
from .database import db

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Chave para assinar os tokens JWT
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-123')
    
    db.init_app(app)
    
    with app.app_context():
        from . import routes, models
        app.register_blueprint(routes.auth_bp)
        db.create_all() # Cria o users.db se não existir
        
    return app