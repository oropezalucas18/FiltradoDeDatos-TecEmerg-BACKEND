from fastapi import APIRouter, Depends, HTTPException
from app.application.reports_usecase import ReportsUseCase
from app.dependencies import auth_guard

router = APIRouter(prefix="/reports")

# Roles con permiso:
PERMISSIONS = ["REPORTS", "ANALYTICS"]

@router.get("/{tipo}")
def list_reports(
    tipo: str,
    user=Depends(auth_guard(PERMISSIONS)),
    usecase: ReportsUseCase = Depends()
):
    if tipo not in ["CO2", "Sonido", "Soterrado"]:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    try:
        reports = usecase.list_sensor_reports(tipo)
        return {
            "sensor": tipo,
            "total": len(reports),
            "reports": reports
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{tipo}/download/{filename}")
def download_report(
    tipo: str,
    filename: str,
    user=Depends(auth_guard(PERMISSIONS)),
    usecase: ReportsUseCase = Depends()
):
    if tipo not in ["CO2", "Sonido", "Soterrado"]:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    try:
        url = usecase.get_download_url(tipo, filename)
        return {
            "filename": filename,
            "url": url
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
