from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.repositories import UserRepository

auth_bp = Blueprint('auth', __name__)
user_repo = UserRepository()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validasi input
        if not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validasi format email
        if '@' not in data['email']:
            return jsonify({'error': 'Invalid email format'}), 400
            
        # Validasi panjang password
        if len(data['password']) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
            
        # Cek username dan email sudah ada atau belum
        if user_repo.get_user_by_username(data['username']):
            return jsonify({'error': 'Username already exists'}), 400
        if user_repo.get_user_by_email(data['email']):
            return jsonify({'error': 'Email already exists'}), 400
            
        # Buat user baru
        user = user_repo.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['username', 'password']):
            return jsonify({'error': 'Missing username or password'}), 400
            
        user = user_repo.get_user_by_username(data['username'])
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
            
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 