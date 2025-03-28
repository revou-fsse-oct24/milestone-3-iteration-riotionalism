from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from app.models import db, User

load_dotenv()

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes.user_route import user_bp
    from app.routes.account_route import account_bp
    from app.routes.transaction_route import transaction_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(transaction_bp)
    
    return app
