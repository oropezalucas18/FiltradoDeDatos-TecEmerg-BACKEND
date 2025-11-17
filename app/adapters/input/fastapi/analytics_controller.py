from fastapi import APIRouter, Depends, HTTPException
from app.application.analytics_usecase import AnalyticsUseCase
from app.infrastructure.query_repository import QueryRepository
from app.dependencies import auth_guard

router = APIRouter(prefix="/analytics")

PERMISSIONS = ["ANALYTICS", "REPORTS"]


@router.get("/{tipo}/stats", response_model=None)
def basic_stats(
    tipo: str,
    limit: int = 200,
    user=Depends(auth_guard(PERMISSIONS)),
):
    if tipo not in ["CO2", "Sonido", "Soterrado"]:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    repo = QueryRepository()
    usecase = AnalyticsUseCase(repo)

    return {
        "sensor": tipo,
        "stats": usecase.basic_stats(tipo, limit)
    }


@router.get("/{tipo}/timeseries/{field}", response_model=None)
def timeseries(
    tipo: str,
    field: str,
    limit: int = 200,
    user=Depends(auth_guard(PERMISSIONS)),
):
    if tipo not in ["CO2", "Sonido", "Soterrado"]:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    repo = QueryRepository()
    usecase = AnalyticsUseCase(repo)

    ts = usecase.time_series(tipo, field, limit)

    if len(ts) == 0:
        raise HTTPException(status_code=404, detail="No hay datos suficientes")

    return {
        "sensor": tipo,
        "field": field,
        "points": ts
    }
