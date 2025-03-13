from flask import jsonify, request
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
    def get_current_user():
        # Sementara hardcode user_id = 1
        user = user_repository.get_by_id(1)
        if user:
            return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404

    @staticmethod
    def update_current_user():
        try:
            data = request.get_json()
            # Sementara hardcode user_id = 1
            user = user_repository.update(1, data)
            if user:
                return jsonify({
                    "message": "User updated successfully",
                    "data": user
                }), 200
            return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
