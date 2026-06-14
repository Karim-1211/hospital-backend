import tkinter as tk
from tkinter import messagebox
from app.services.patient_service import PatientService
from app.services.appointment_service import AppointmentService
from app.services.doctor_service import DoctorService


class BookingForm:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Book Appointment")
        self.window.geometry("400x400")

        self.patient_service = PatientService()
        self.appointment_service = AppointmentService()
        self.doctor_service = DoctorService()

        # Doctor dropdown
        tk.Label(self.window, text="Select Doctor").pack()
        self.doctors = self.doctor_service.get_all_doctors()
        self.doctor_var = tk.StringVar()
        self.doctor_menu = tk.OptionMenu(
            self.window,
            self.doctor_var,
            *[d[1] for d in self.doctors]
        )
        self.doctor_menu.pack()

        # Patient name
        tk.Label(self.window, text="Patient Name").pack()
        self.patient_entry = tk.Entry(self.window)
        self.patient_entry.pack()

        # Date
        tk.Label(self.window, text="Date").pack()
        self.date_entry = tk.Entry(self.window)
        self.date_entry.pack()

        # Time
        tk.Label(self.window, text="Time").pack()
        self.time_entry = tk.Entry(self.window)
        self.time_entry.pack()

        tk.Button(self.window, text="Book Appointment", command=self.book).pack()

    def book(self):
        doctor_name = self.doctor_var.get()
        patient_name = self.patient_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()

        if not patient_name:
            messagebox.showerror("Error", "Patient name required")
            return

        # create patient first
        patient_id = self.patient_service.create_patient(patient_name)

        # find doctor id
        doctor_id = None
        for d in self.doctors:
            if d[1] == doctor_name:
                doctor_id = d[0]

        if not doctor_id:
            messagebox.showerror("Error", "Select doctor")
            return

        self.appointment_service.create_appointment(
            doctor_id,
            patient_id,
            date,
            time
        )

        messagebox.showinfo("Success", "Appointment Booked")