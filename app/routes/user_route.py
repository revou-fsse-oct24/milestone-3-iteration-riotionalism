from flask import Blueprint
from app.views.user_view import UserView

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    return UserView.create_user()

@user_bp.route('/users/me', methods=['GET'])
def get_current_user():
    return UserView.get_current_user()

@user_bp.route('/users/me', methods=['PUT'])
def update_current_user():
    return UserView.update_current_user()
