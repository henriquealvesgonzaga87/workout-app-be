from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    is_active: bool
    is_super_admin: bool
    creation_date: datetime
    update_date: datetime | None
