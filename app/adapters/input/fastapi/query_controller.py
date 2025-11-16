from fastapi import APIRouter, Depends, HTTPException
from app.application.query_usecase import QueryUseCase
from app.dependencies import auth_guard

router = APIRouter(prefix="/query")

# Roles con permiso de consulta:
PERMISSIONS = ["QUERY", "REPORTS", "ANALYTICS"]

@router.get("/{tipo}")
def query_last(
    tipo: str,
    limit: int = 50,
    user=Depends(auth_guard(PERMISSIONS)),
    usecase: QueryUseCase = Depends()
):
    if tipo not in ["CO2", "Sonido", "Soterrado"]:
        raise HTTPException(status_code=400, detail="Tipo de sensor inválido")

    return {
        "sensor": tipo,
        "limit": limit,
        "data": usecase.get_last_records(tipo, limit)
    }
