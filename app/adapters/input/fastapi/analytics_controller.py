from app.adapters.output.firebase_repository import FirebaseRepository
from fastapi import APIRouter, Depends, HTTPException
from app.application.analytics_usecase import AnalyticsUseCase
from app.infrastructure.query_repository import QueryRepository
from app.dependencies import auth_guard

router = APIRouter(prefix="/analytics")

PERMISSIONS = ["ANALYTICS", "REPORTS","ADMIN"]


@router.get("/{tipo}/stats")
def basic_stats(tipo: str, limit: int = 200, user=Depends(auth_guard(PERMISSIONS))):
    tipo = tipo.lower()
    if tipo not in ["co2", "sonido", "soterrado"]:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    repo = FirebaseRepository()
    usecase = AnalyticsUseCase(repo)

    return usecase.basic_stats(tipo, limit)


@router.get("/{tipo}/timeseries/{field}", response_model=None)
def timeseries(
    tipo: str,
    field: str,
    limit: int = 200,
    user=Depends(auth_guard(PERMISSIONS)),
):
    tipo = tipo.lower()

    if tipo not in ["co2", "sonido", "soterrado"]:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    # 🔥 Ahora usamos FirebaseRepository en vez de QueryRepository
    repo = FirebaseRepository()
    usecase = AnalyticsUseCase(repo)

    ts = usecase.time_series(tipo, field, limit)

    if not ts:
        raise HTTPException(status_code=404, detail="No hay datos suficientes")

    return {
        "sensor": tipo,
        "field": field,
        "points": ts
    }
