from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories import UserRepository

user_bp = Blueprint('user', __name__)
user_repo = UserRepository()

@user_bp.route('/users', methods=['POST'])
def create_user():
    return UserView.create_user()

@user_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        # Convert jwt identity ke integer
        current_user_id = int(get_jwt_identity())
        user = user_repo.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    try:
        # Convert jwt identity ke integer
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if 'password' in data:
            return jsonify({'error': 'Cannot update password through this endpoint'}), 400
            
        user = user_repo.update_user(current_user_id, data)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'updated_at': user.updated_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
