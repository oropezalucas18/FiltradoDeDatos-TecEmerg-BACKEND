from typing import List
from app.infrastructure.supabase_client import supabase_client
from app.infrastructure.config import settings

class ReportService:

    BUCKET = settings.SUPABASE_BUCKET  # "reportes"

    def list_reports(self, sensor_type: str) -> List[str]:
        """
        Lista todos los PDFs disponibles para un sensor.
        Supabase almacena así:
        reportes/{sensor_type}/archivo.pdf
        """
        res = supabase_client.storage.from_(self.BUCKET).list(sensor_type)
        if res is None:
            return []
        return [item["name"] for item in res]

    def get_report_url(self, sensor_type: str, filename: str) -> str:
        """
        Retorna una URL pública o firmada para descargar un reporte.
        """
        path = f"{sensor_type}/{filename}"
        return supabase_client.storage.from_(self.BUCKET).get_public_url(path)
