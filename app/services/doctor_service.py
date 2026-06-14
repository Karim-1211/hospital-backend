from app.database.db import engine
from sqlalchemy import text


class DoctorService:

    def get_all_doctors(self):
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT id, name, specialization FROM doctors")
            )
            return result.fetchall()
