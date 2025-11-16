from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    email: str
    role: str
    password_hash: str
    creado_por: Optional[str]
    creado_el: Optional[str]
    activo: bool = True
