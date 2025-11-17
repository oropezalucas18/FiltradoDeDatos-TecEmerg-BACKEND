from fastapi import APIRouter, Depends, HTTPException
from app.application.query_usecase import QueryUseCase
from app.infrastructure.query_repository import QueryRepository
from app.dependencies import auth_guard

router = APIRouter(prefix="/query")

PERMISSIONS = ["QUERY", "REPORTS", "ANALYTICS"]


@router.get("/{tipo}", response_model=None)
def query_last(
    tipo: str,
    limit: int = 50,
    user=Depends(auth_guard(PERMISSIONS)),
):
    if tipo not in ["CO2", "Sonido", "Soterrado"]:
        raise HTTPException(status_code=400, detail="Tipo de sensor inválido")

    repo = QueryRepository()
    usecase = QueryUseCase(repo)

    return {
        "sensor": tipo,
        "limit": limit,
        "data": usecase.get_last_records(tipo, limit)
    }
