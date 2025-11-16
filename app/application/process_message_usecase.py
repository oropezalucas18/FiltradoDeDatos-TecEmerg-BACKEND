import pandas as pd
from app.domain.entities.sensor_data import SensorData
from app.domain.services.cleaner_service import CleanerService
from app.domain.services.sensor_validator import SensorValidator
from app.domain.services.report_service import ReportService
from app.adapters.output.firebase_repository import FirebaseRepository
from app.adapters.output.supabase_repository import SupabaseRepository
from worker.report_generator import ReportGenerator


class ProcessMessageUseCase:

    def __init__(self):
        self.firebase_repo = FirebaseRepository()
        self.supabase_repo = SupabaseRepository()
        self.report_service = ReportService()
        self.report_generator = ReportGenerator()

    # ==============================
    # EJECUTAR PROCESO COMPLETO
    # ==============================
    def execute(self, message: dict):
        """
        Proceso completo para manejar un mensaje proveniente de RabbitMQ.
        Incluye:
        - validación
        - limpieza
        - normalización
        - guardado en Firebase
        - backup en Supabase
        - generación de PDF
        - subida del PDF a Supabase Storage
        """

        tipo = message["tipo"]
        rows = message["rows"]
        origen = message.get("origen", "archivo")

        # Convertir a DataFrame
        df = pd.DataFrame(rows)

        # VALIDACIÓN
        SensorValidator.validar_campos(tipo, df)

        # LIMPIEZA Y NORMALIZACIÓN
        df = CleanerService.clean(df)
        df = CleanerService.normalize(df)

        # Guardado principal y backup
        self._save_records(tipo, df, origen)

        # Generar reporte
        pdf_path = self.report_generator.generate(tipo, df)

        # Subir reporte
        self.supabase_repo.upload_report(tipo, pdf_path)

        return True

    # ==============================
    # MÉTODO INTERNO: GUARDAR REGISTROS
    # ==============================
    def _save_records(self, tipo: str, df: pd.DataFrame, origen: str):
        """
        Guarda cada fila del DataFrame en:
        - Firebase (principal)
        - Supabase (backup)
        """
        for row in df.to_dict(orient="records"):
            sensor_data = SensorData(
                tipo=tipo,
                valores=row,
                timestamp=row.get("timestamp"),
                origen=origen,
                procesado=True
            )

            self.firebase_repo.save(sensor_data)
            self.supabase_repo.save({
                "tipo": tipo,
                "valores": row,
                "timestamp": row.get("timestamp")
            })
