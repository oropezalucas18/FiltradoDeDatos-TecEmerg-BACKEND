from fastapi import Depends, HTTPException, Header
from app.domain.services.auth_service import AuthService
from app.infrastructure.config import settings
from app.adapters.output.firebase_user_repository import FirebaseUserRepository
from app.domain.entities.role import PERMISSIONS

user_repo = FirebaseUserRepository()

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Falta el token Authorization")

    try:
        token = authorization.replace("Bearer ", "")
        payload = AuthService.decode_token(token)
        user = user_repo.get_by_id(payload["sub"])
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


def auth_guard(required_permissions: list):
    def guard(user=Depends(get_current_user)):
        role = user.role

        # ADMIN puede hacer todo
        if role == "ADMIN":
            return user

        # Revisa permisos
        allowed = PERMISSIONS.get(role, [])
        for perm in required_permissions:
            if perm in allowed:
                return user

        raise HTTPException(status_code=403, detail="No tienes permisos")
    return guard
