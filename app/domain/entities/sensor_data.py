from pydantic import BaseModel
from typing import Optional, Dict, Any

class SensorData(BaseModel):
    tipo: str        # CO2 | Sonido | Soterrado
    valores: Dict[str, Any]    # Campos del sensor dentro de "valores"
    timestamp: Optional[str]    # Timestamp del registro
    origen: str = "archivo"      # archivo | iot | realtime
    procesado: bool = False      # El worker lo marcará como True