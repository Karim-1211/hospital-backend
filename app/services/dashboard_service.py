from app.database.db import engine
from sqlalchemy import text


class DashboardService:

    def get_all_appointments(self):
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    a.id,
                    d.name AS doctor,
                    p.name AS patient,
                    a.appointment_date,
                    a.appointment_time,
                    COALESCE(a.status, 'Pending') AS status
                FROM appointments a
                LEFT JOIN doctors d ON a.doctor_id = d.id
                LEFT JOIN patients p ON a.patient_id = p.id
                ORDER BY a.id DESC
            """))
            return result.fetchall()

    def delete_appointment(self, appointment_id):
        with engine.begin() as conn:
            conn.execute(
                text("DELETE FROM appointments WHERE id = :id"),
                {"id": appointment_id}
            )