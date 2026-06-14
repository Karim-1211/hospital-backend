from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import engine
from app.database.base import Base
from app.models.user import User
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.department import Department
from app.models.appointment import Appointment
from sqlalchemy import text
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Hospital Appointment System API")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")

# ─── MODELS ───────────────────────────────────────────────

class PatientModel(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    date_of_birth: Optional[str] = None

class DoctorModel(BaseModel):
    name: str
    specialization: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class AppointmentModel(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: str
    appointment_time: str

class DepartmentModel(BaseModel):
    name: str

class LoginModel(BaseModel):
    username: str
    password: str

# ─── LOGIN ────────────────────────────────────────────────

@app.post("/login")
def login(data: LoginModel):
    # Simple login — you can change username/password here
    if data.username == "admin" and data.password == "admin123":
        return {"message": "Login successful", "token": "hospital-token-2026"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

# ─── PATIENTS ─────────────────────────────────────────────

@app.get("/patients")
def get_patients():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM patients"))
            rows = result.mappings().all()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/patients")
def create_patient(data: PatientModel):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO patients (name, phone, email, date_of_birth)
                    VALUES (:name, :phone, :email, :date_of_birth)
                """),
                data.model_dump()
            )
        return {"message": "Patient created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, data: PatientModel):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    UPDATE patients
                    SET name=:name, phone=:phone,
                        email=:email, date_of_birth=:date_of_birth
                    WHERE id=:id
                """),
                {**data.model_dump(), "id": patient_id}
            )
        return {"message": "Patient updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("DELETE FROM patients WHERE id=:id"),
                {"id": patient_id}
            )
        return {"message": "Patient deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── DOCTORS ──────────────────────────────────────────────

@app.get("/doctors")
def get_doctors():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM doctors"))
            rows = result.mappings().all()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/doctors")
def create_doctor(data: DoctorModel):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO doctors (name, specialization, phone, email)
                    VALUES (:name, :specialization, :phone, :email)
                """),
                data.model_dump()
            )
        return {"message": "Doctor created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, data: DoctorModel):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    UPDATE doctors
                    SET name=:name, specialization=:specialization,
                        phone=:phone, email=:email
                    WHERE id=:id
                """),
                {**data.model_dump(), "id": doctor_id}
            )
        return {"message": "Doctor updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("DELETE FROM doctors WHERE id=:id"),
                {"id": doctor_id}
            )
        return {"message": "Doctor deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── APPOINTMENTS ─────────────────────────────────────────

@app.get("/appointments")
def get_appointments():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT a.id,
                       p.name as patient_name,
                       d.name as doctor_name,
                       a.appointment_date,
                       a.appointment_time,
                       a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors  d ON a.doctor_id  = d.id
            """))
            rows = result.mappings().all()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/appointments")
def create_appointment(data: AppointmentModel):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO appointments
                    (doctor_id, patient_id, appointment_date, appointment_time, status)
                    VALUES (:doctor_id, :patient_id, :appointment_date,
                            :appointment_time, 'Pending')
                """),
                data.model_dump()
            )
        return {"message": "Appointment created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("DELETE FROM appointments WHERE id=:id"),
                {"id": appointment_id}
            )
        return {"message": "Appointment deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── DEPARTMENTS ──────────────────────────────────────────

@app.get("/departments")
def get_departments():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM departments"))
            rows = result.mappings().all()
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/departments")
def create_department(data: DepartmentModel):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO departments (name) VALUES (:name)"),
                data.model_dump()
            )
        return {"message": "Department created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/departments/{department_id}")
def delete_department(department_id: int):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("DELETE FROM departments WHERE id=:id"),
                {"id": department_id}
            )
        return {"message": "Department deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))