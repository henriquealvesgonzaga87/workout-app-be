from dataclasses import dataclass
from datetime import datetime


@dataclass
class TrainingTypes:
    id: int
    name: str
    created_at: datetime
    update_date: datetime | None
