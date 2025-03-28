from flask import jsonify, request
from flask_login import current_user, login_required
from app.repositories.user_repository import UserRepository

class UserView:
    @staticmethod
    def create_user():
        try:
            data = request.get_json()
            required_fields = ['username', 'email', 'password']
            
            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400
                
            user = UserRepository.create(data)
            return jsonify({
                "message": "User created successfully",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def login():
        try:
            data = request.get_json()
            if not all(k in data for k in ['email', 'password']):
                return jsonify({"error": "Missing email or password"}), 400

            user = UserRepository.login(data['email'], data['password'])
            if user:
                return jsonify({
                    "message": "Login successful",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    }
                }), 200
            return jsonify({"error": "Invalid credentials"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    @login_required
    def get_current_user():
        return jsonify({
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }), 200

    @staticmethod
    @login_required
    def update_current_user():
        try:
            data = request.get_json()
            user = UserRepository.update(current_user.id, data)
            if user:
                return jsonify({
                    "message": "User updated successfully",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    }
                }), 200
            return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400
