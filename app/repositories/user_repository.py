from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

class UserRepository:
    def create_user(self, username, email, password):
        try:
            # Validasi email dan username unik
            if self.get_user_by_email(email):
                raise ValueError("Email already exists")
            if self.get_user_by_username(username):
                raise ValueError("Username already exists")

            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)

    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def update_user(self, user_id, data):
        try:
            user = self.get_user_by_id(user_id)
            if user:
                for key, value in data.items():
                    setattr(user, key, value)
                db.session.commit()
                return user
            return None
        except Exception as e:
            db.session.rollback()
            raise e

    # Method baru untuk verifikasi password
    def verify_password(self, user, password):
        return check_password_hash(user.password_hash, password)
