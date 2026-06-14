import os
import jwt
import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import engine
from app.database.base import Base
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.department import Department
from app.models.appointment import Appointment
from sqlalchemy import text
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Hospital Appointment System API")

# ── CORS ─────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── STARTUP ──────────────────────────────────────────────
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")

# ── AUTH CONFIG ──────────────────────────────────────────
SECRET_KEY     = os.getenv("SECRET_KEY", "hospital-secret-key-2026")
ALGORITHM      = "HS256"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ── MODELS ───────────────────────────────────────────────
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

# ── LOGIN ────────────────────────────────────────────────
@app.post("/login")
def login(data: LoginModel):
    if data.username != ADMIN_USERNAME or data.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    payload = {
        "sub": data.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"message": "Login successful", "token": token}

# ── PATIENTS ─────────────────────────────────────────────
@app.get("/patients")
def get_patients():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM patients"))
            return [dict(row) for row in result.mappings().all()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/patients")
def create_patient(data: PatientModel):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO patients (name, phone, email, date_of_birth) VALUES (:name, :phone, :email, :date_of_birth)"),
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
                text("UPDATE patients SET name=:name, phone=:phone, email=:email, date_of_birth=:date_of_birth WHERE id=:id"),
                {**data.model_dump(), "id": patient_id}
            )
        return {"message": "Patient updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    try:
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM patients WHERE id=:id"), {"id": patient_id})
        return {"message": "Patient deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── DOCTORS ──────────────────────────────────────────────
@app.get("/doctors")
def get_doctors():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM doctors"))
            return [dict(row) for row in result.mappings().all()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/doctors")
def create_doctor(data: DoctorModel):
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO doctors (name, specialization, phone, email) VALUES (:name, :specialization, :phone, :email)"),
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
                text("UPDATE doctors SET name=:name, specialization=:specialization, phone=:phone, email=:email WHERE id=:id"),
                {**data.model_dump(), "id": doctor_id}
            )
        return {"message": "Doctor updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500,