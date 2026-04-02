from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.infrastructure.schemas import Base


class UserSchema(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_super_admin = Column(Boolean, default=False)
    creation_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=True)

    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}"
