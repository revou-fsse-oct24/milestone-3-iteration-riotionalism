from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    from app.routes.user_route import user_bp
    from app.routes.account_route import account_bp
    from app.routes.transaction_route import transaction_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(transaction_bp)
    
    return app
