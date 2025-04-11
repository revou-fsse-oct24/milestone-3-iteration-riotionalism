from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from datetime import datetime, timedelta
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to RevoBank API',
            'version': '1.0'
        })
    
    # Konfigurasi Database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'revobank.db'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Konfigurasi JWT yang lebih aman
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-super-secret-key-change-this')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=3)  # Token expired dalam 3 jam
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # refresh token valid 30 hari
    app.config['JWT_ERROR_MESSAGE_KEY'] = 'error'
    
    # Inisialisasi
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Simpan token yang sudah di-blacklist
    app.jwt_blocklist = set()  # simpan di app context
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in app.jwt_blocklist
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.account_routes import account_bp
    from app.routes.transaction_routes import transaction_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(account_bp, url_prefix='/api')
    app.register_blueprint(transaction_bp, url_prefix='/api')
    
    with app.app_context():
        db.create_all()
    
    return app
