from app.domain.services.report_service import ReportService

class ReportsUseCase:

    def __init__(self):
        self.service = ReportService()

    def list_sensor_reports(self, sensor_type: str):
        return self.service.list_reports(sensor_type)

    def get_download_url(self, sensor_type: str, filename: str):
        reports = self.service.list_reports(sensor_type)

        if filename not in reports:
            raise Exception("Reporte no encontrado")

        return self.service.get_report_url(sensor_type, filename)
