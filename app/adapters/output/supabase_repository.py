from app.infrastructure.supabase_client import supabase_client
from app.infrastructure.config import settings

class SupabaseRepository:

    TABLE = "sensores"  # tu tabla en Supabase

    def save(self, data: dict):
        """
        Guarda respaldo en Supabase.
        Estructura:
        {
            tipo: "CO2",
            valores: {...},
            timestamp: "2024-01-01T12:00:00"
        }
        """
        supabase_client.table(self.TABLE).insert(data).execute()

    def upload_report(self, sensor_type: str, file_path: str):
        """
        Sube un PDF generado por el worker al bucket "reportes".
        Ruta final:
        reportes/{sensor_type}/{archivo}.pdf
        """
        bucket = settings.SUPABASE_BUCKET
        file_name = file_path.split("/")[-1]

        with open(file_path, "rb") as f:
            supabase_client.storage.from_(bucket).upload(
                f"{sensor_type}/{file_name}",
                f.read(),
                file_options={"content-type": "application/pdf"}
            )

        return f"{bucket}/{sensor_type}/{file_name}"
