from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.database.base import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String)
    specialization = Column(String)

    department_id = Column(Integer, ForeignKey("departments.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
