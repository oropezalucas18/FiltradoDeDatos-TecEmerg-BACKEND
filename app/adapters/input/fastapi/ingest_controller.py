from fastapi import APIRouter, UploadFile, Depends, HTTPException, File
from app.application.ingest_usecase import IngestUseCase
from app.dependencies import auth_guard
from app.dependencies import get_ingest_usecase

router = APIRouter(prefix="/ingest")

# Solo OPERADOR o ADMIN pueden ingresar datos
PERMISSIONS = ["INGEST"]

@router.post("/{tipo}", response_model=None)
async def ingest(
    tipo: str,
    file: UploadFile = File(...),
    usecase: IngestUseCase = Depends(get_ingest_usecase)
):
    """
    Sube un archivo .csv / .xlsx / .txt de un sensor.
    Lo parsea con Spark y lo manda a RabbitMQ.
    """

    if tipo not in ["CO2", "Sonido", "Soterrado"]:
        raise HTTPException(status_code=400, detail="Tipo de sensor inválido")

    try:
        rows = usecase.extract_rows(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error procesando archivo: {e}")

    usecase.publish_to_queue(tipo, rows, "system@test.com")

    return {
        "status": "queued",
        "rows": len(rows),
        "sensor": tipo
    }