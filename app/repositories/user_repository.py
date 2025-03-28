from app.models import db, User
from flask_login import login_user, logout_user

class UserRepository:
    @staticmethod
    def create(user_data):
        user = User(
            username=user_data['username'],
            email=user_data['email']
        )
        user.set_password(user_data['password'])
        
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def update(user_id, user_data):
        user = User.query.get(user_id)
        if user:
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            if 'password' in user_data:
                user.set_password(user_data['password'])
            db.session.commit()
        return user

    @staticmethod
    def login(email, password):
        user = UserRepository.get_by_email(email)
        if user and user.check_password(password):
            login_user(user)
            return user
        return None

    @staticmethod
    def logout():
        logout_user()
