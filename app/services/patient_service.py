from app.database.db import engine
from sqlalchemy import text


class PatientService:

    def create_patient(self, name):
        with engine.begin() as conn:
            result = conn.execute(
                text("INSERT INTO patients (name) VALUES (:name) RETURNING id"),
                {"name": name}
            )
            return result.fetchone()[0]