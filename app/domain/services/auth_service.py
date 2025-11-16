import bcrypt
import jwt
from datetime import datetime, timedelta
from app.infrastructure.config import settings

class AuthService:

    @staticmethod
    def verify_password(password, hashed):
        return bcrypt.checkpw(password.encode(), hashed.encode())

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def generate_token(user):
        payload = {
            "sub": user.id,
            "email": user.email,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(hours=10)
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
