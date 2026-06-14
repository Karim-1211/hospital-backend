import tkinter as tk
from tkinter import ttk
from app.services.dashboard_service import DashboardService


class AdminDashboard:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Admin Dashboard")
        self.window.geometry("700x400")

        self.dashboard_service = DashboardService()

        self.tree = ttk.Treeview(
            self.window,
            columns=("id", "doctor", "patient", "date", "time", "status"),
            show="headings"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("doctor", text="Doctor")
        self.tree.heading("patient", text="Patient")
        self.tree.heading("date", text="Date")
        self.tree.heading("time", text="Time")
        self.tree.heading("status", text="Status")

        self.tree.pack(fill="both", expand=True)

        self.load_data()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())

        data = self.dashboard_service.get_all_appointments()

        for row in data:
            self.tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                )
            )