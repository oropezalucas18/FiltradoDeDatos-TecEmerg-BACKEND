from pydantic import BaseModel
from typing import Optional, Dict, Any

class SensorData(BaseModel):
    tipo: str        # CO2 | Sonido | Soterrado
    data: Dict[str, Any]
    timestamp: Optional[str]