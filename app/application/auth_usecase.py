from uuid import uuid4
from app.domain.services.auth_service import AuthService
from app.domain.entities.user import User

class AuthUseCase:

    def __init__(self, user_repo):
        self.user_repo = user_repo

    def login(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        if not user:
            return None

        if not AuthService.verify_password(password, user.password_hash):
            return None

        token = AuthService.generate_token(user)
        return token, user

    def register(self, email: str, password: str, role: str, created_by: str):
        hashed = AuthService.hash_password(password)
        new_user = User(
            id=str(uuid4()),
            email=email,
            role=role,
            password_hash=hashed,
            creado_por=created_by,
            creado_el="",
            activo=True
        )
        self.user_repo.save(new_user)
        return new_user
