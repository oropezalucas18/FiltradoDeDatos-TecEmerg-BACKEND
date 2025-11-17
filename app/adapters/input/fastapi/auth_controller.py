from app.adapters.output.firebase_user_repository import FirebaseUserRepository
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from app.application.auth_usecase import AuthUseCase
from app.dependencies import auth_guard
from app.domain.entities.user import User

router = APIRouter(prefix="/auth")

class DisableUserDTO(BaseModel):
    user_id: str


class UpdateRoleDTO(BaseModel):
    user_id: str
    new_role: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    names: str
    lastnames: str
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
def register(
    req: RegisterRequest,
    current_user: User = Depends(auth_guard(["ADMIN"])),   # 🔒 SOLO ADMIN
    usecase = AuthUseCase(FirebaseUserRepository())
):
    valid_roles = ["ADMIN", "ANALISTA", "OPERADOR", "INVITADO"]
    if req.role not in valid_roles:
        raise HTTPException(400, "Rol inválido")

    return usecase.register(
        req.email,
        req.password,
        req.names,
        req.lastnames,
        req.role
    )


@router.post("/login")
def login(
    req: LoginRequest,
        usecase = AuthUseCase(FirebaseUserRepository())
):
    return usecase.login(req.email, req.password)

# =============================
# 1) DESHABILITAR USUARIO
# =============================
@router.patch("/disable")
def disable_user(
    data: DisableUserDTO,
    current_user: User = Depends(auth_guard(["ADMIN"])),
    usecase: AuthUseCase = Depends()
):
    try:
        usecase.disable_user(data.user_id)
        return {"status": "ok", "message": "Usuario deshabilitado"}
    except Exception as e:
        raise HTTPException(400, detail=str(e))


# =============================
# 2) LISTAR USUARIOS (solo admin)
# =============================
@router.get("/users")
def list_users(
    current_user: User = Depends(auth_guard(["ADMIN"])),
    usecase = AuthUseCase(FirebaseUserRepository())
):
    try:
        return usecase.list_users()
    except Exception as e:
        raise HTTPException(400, detail=str(e))


# =============================
# 3) CAMBIAR ROL DE USUARIO
# =============================
@router.patch("/update-role")
def update_role(
    data: UpdateRoleDTO,
    current_user: User = Depends(auth_guard(["ADMIN"])),
    usecase = AuthUseCase(FirebaseUserRepository())
):
    valid_roles = ["ADMIN", "ANALISTA", "OPERADOR", "INVITADO"]
    
    if data.new_role not in valid_roles:
        raise HTTPException(400, "Rol inválido")

    try:
        usecase.update_role(data.user_id, data.new_role)
        return {"status": "ok", "message": "Rol actualizado"}
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@router.get("/hash/{password}")
def hash_password(password: str):
    from app.domain.services.auth_service import AuthService
    return {"hash": AuthService.hash_password(password)}