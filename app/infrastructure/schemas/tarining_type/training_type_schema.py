from sqlalchemy import Column, DateTime, Integer, String

from app.infrastructure.schemas import Base


class TrainingTypeSchema(Base):
    __tablename__ = "training_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    creation_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=True)

    def __str__(self):
        return f"Traning Type(id={self.id}, name={self.name})"
