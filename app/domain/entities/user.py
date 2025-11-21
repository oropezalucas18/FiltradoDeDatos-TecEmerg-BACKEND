from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: str
    email: str
    password: str
    names: str
    lastnames: str
    role: str
    status: str = "enabled"
    created_at: datetime = None
