from fastapi import APIRouter, UploadFile, Depends, HTTPException
from app.application.ingest_usecase import IngestUseCase
from app.dependencies import auth_guard

router = APIRouter(prefix="/ingest")

# Solo OPERADOR o ADMIN pueden ingresar datos
PERMISSIONS = ["INGEST"]

@router.post("/{tipo}")
async def ingest(
    tipo: str,
    file: UploadFile,
    user=Depends(auth_guard(PERMISSIONS)),
    usecase: IngestUseCase = Depends()
):
    """
    Endpoint principal para subir archivos de sensores.
    Solo pueden acceder OPERADOR y ADMIN.
    """

    # Validamos tipo de sensor
    if tipo not in ["CO2", "Sonido", "Soterrado"]:
        raise HTTPException(status_code=400, detail="Tipo de sensor inválido")

    # Extraer filas con Pandas o Spark
    try:
        rows = usecase.extract_rows(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error procesando archivo: {e}")

    # Enviar a RabbitMQ
    usecase.publish_to_queue(tipo, rows, user.email)

    return {
        "status": "queued",
        "rows": len(rows),
        "sensor": tipo,
        "mensaje": "Archivo enviado al worker para procesamiento"
    }
