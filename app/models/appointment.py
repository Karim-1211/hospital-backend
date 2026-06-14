from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.database.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))

    appointment_date = Column(String)
    appointment_time = Column(String)

    status = Column(String, default="Pending")
    notes = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
