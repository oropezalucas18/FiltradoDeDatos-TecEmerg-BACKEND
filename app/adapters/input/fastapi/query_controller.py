from app.adapters.output.firebase_repository import FirebaseRepository
from fastapi import APIRouter, Depends, HTTPException
from app.application.query_usecase import QueryUseCase
from app.infrastructure.query_repository import QueryRepository
from app.dependencies import auth_guard

router = APIRouter(prefix="/query")

PERMISSIONS = ["QUERY", "REPORTS", "ANALYTICS", "ADMIN"]


@router.get("/{tipo}")
def query_last(tipo: str, limit: int = 50, user=Depends(auth_guard(PERMISSIONS))):
    tipo = tipo.lower()
    if tipo not in ["co2", "sonido", "soterrado"]:
        raise HTTPException(status_code=400, detail="Tipo de sensor inválido")

    repo = FirebaseRepository()
    usecase = QueryUseCase(repo)

    return {
        "sensor": tipo,
        "data": usecase.get_last_records(tipo, limit)
    }