from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Konfigurasi Database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'revobank.db'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Konfigurasi JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'rahasia-jwt')  # Gunakan env variable di production
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
    
    # Inisialisasi
    db.init_app(app)
    jwt.init_app(app)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Import dan register blueprints
    from app.routes import auth_bp, account_bp, transaction_bp, user_bp
    
    # Register blueprints dengan prefix
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(account_bp, url_prefix='/api/accounts')
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    
    with app.app_context():
        db.create_all()
    
    return app
