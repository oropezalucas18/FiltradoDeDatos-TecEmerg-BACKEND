# app/dependencies.py

from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from app.infrastructure.config import settings
from app.domain.services.auth_service import AuthService
from app.adapters.output.firebase_user_repository import FirebaseUserRepository
from app.adapters.output.rabbitmq_queue import RabbitMQQueue
from app.application.ingest_usecase import IngestUseCase
from app.domain.entities.role import PERMISSIONS


# =====================================================
# FACTORÍA DEL REPOSITORIO DE USUARIOS
# =====================================================
def get_user_repo():
    return FirebaseUserRepository()


# =====================================================
# VALIDAR TOKEN Y OBTENER USUARIO
# =====================================================
def get_current_user(
    authorization: str = Header(None),
    repo: FirebaseUserRepository = Depends(get_user_repo)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Falta el token Authorization")

    try:
        token = authorization.replace("Bearer ", "")
        payload = AuthService.decode_token(token)

        user = repo.get_by_id(payload["sub"])
        if not user:
            raise HTTPException(401, "Usuario no encontrado")

        return user

    except Exception:
        raise HTTPException(401, detail="Token inválido o expirado")


# =====================================================
# GUARD GENERAL PARA ROLES
# =====================================================
security = HTTPBearer()

def auth_guard(roles: list = None):
    def wrapper(
        credentials=Depends(security),
        repo: FirebaseUserRepository = Depends(get_user_repo)
    ):
        token = credentials.credentials

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("sub")

            if not user_id:
                raise HTTPException(401, "Token sin 'sub'.")

            user = repo.get_by_id(user_id)
            if not user:
                raise HTTPException(401, "Usuario no encontrado.")

            if user.status != "enabled":
                raise HTTPException(403, "Usuario deshabilitado.")

            if roles and user.role not in roles:
                raise HTTPException(403, "No autorizado.")

            return user

        except JWTError:
            raise HTTPException(401, "Token inválido o expirado")

    return wrapper


# =====================================================
# INGESTION USECASE
# =====================================================
def get_ingest_usecase():
    from app.adapters.output.spark_file_parser import SparkFileParser
    from app.adapters.output.rabbitmq_queue import RabbitMQQueue
    return IngestUseCase(SparkFileParser(), RabbitMQQueue())


# =====================================================
# GUARD DE PERMISOS ESPECÍFICOS
# =====================================================
def require_permissions(perms: list[str]):
    def wrapper():
        return auth_guard(perms)
    return wrapper
