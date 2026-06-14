from app.database.db import engine
from sqlalchemy import text


class AppointmentService:

    def create_appointment(self, doctor_id, patient_id, date, time):
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO appointments 
                    (doctor_id, patient_id, appointment_date, appointment_time, status)
                    VALUES (:doctor_id, :patient_id, :date, :time, 'Pending')
                """),
                {
                    "doctor_id": doctor_id,
                    "patient_id": patient_id,
                    "date": date,
                    "time": time
                }
            )