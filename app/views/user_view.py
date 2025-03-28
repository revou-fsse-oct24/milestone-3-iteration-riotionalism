from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.user_repository import UserRepository

user_repository = UserRepository()

class UserView:
    @staticmethod
    def create_user():
        try:
            data = request.get_json()
            required_fields = ['username', 'email', 'password']
            
            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400
                
            user = user_repository.create(data)
            return jsonify({
                "message": "User created successfully",
                "data": user
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    @jwt_required()
    def get_current_user():
        try:
            current_user_id = get_jwt_identity()
            user = user_repository.get_user_by_id(current_user_id)
            
            if not user:
                return jsonify({"error": "User not found"}), 404
                
            return jsonify({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    @jwt_required()
    def update_current_user():
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            # Prevent password update through this endpoint
            if 'password' in data:
                return jsonify({"error": "Cannot update password through this endpoint"}), 400
                
            user = user_repository.update_user(current_user_id, data)
            
            if not user:
                return jsonify({"error": "User not found"}), 404
                
            return jsonify({
                "message": "User updated successfully",
                "user": {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'updated_at': user.updated_at.isoformat()
                }
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
