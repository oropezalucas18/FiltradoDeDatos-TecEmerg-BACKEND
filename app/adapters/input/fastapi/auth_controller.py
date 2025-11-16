from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.auth_usecase import AuthUseCase
from app.adapters.output.firebase_user_repository import FirebaseUserRepository
from app.dependencies import auth_guard, get_current_user

router = APIRouter(prefix="/auth")

user_repo = FirebaseUserRepository()
auth_usecase = AuthUseCase(user_repo)


# ================================
# MODELOS
# ================================
class LoginDTO(BaseModel):
    email: str
    password: str


class RegisterDTO(BaseModel):
    email: str
    password: str
    role: str


# ================================
# LOGIN
# ================================
@router.post("/login")
def login(data: LoginDTO):
    token, user = auth_usecase.login(data.email, data.password)

    if not token:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {
        "token": token,
        "user": {
            "email": user.email,
            "role": user.role,
            "id": user.id
        }
    }


# ================================
# REGISTRO (solo ADMIN)
# ================================
@router.post("/register")
def register(
    data: RegisterDTO,
    admin=Depends(auth_guard(["*"]))   # Solo ADMIN puede registrar
):
    if data.role not in ["ADMIN", "ANALISTA", "OPERADOR", "INVITADO"]:
        raise HTTPException(status_code=400, detail="Rol inválido")

    new_user = auth_usecase.register(
        email=data.email,
        password=data.password,
        role=data.role,
        created_by=admin.email
    )

    return {
        "status": "ok",
        "user_id": new_user.id,
        "email": new_user.email,
        "role": new_user.role
    }
