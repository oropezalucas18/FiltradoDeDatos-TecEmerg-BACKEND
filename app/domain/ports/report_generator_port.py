from abc import ABC, abstractmethod

class ReportGeneratorPort(ABC):

    @abstractmethod
    def list_reports(self, sensor_type: str):
        pass

    @abstractmethod
    def get_report_url(self, sensor_type: str, filename: str):
        pass
