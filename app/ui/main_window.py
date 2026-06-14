import tkinter as tk
from app.ui.admin_dashboard import AdminDashboard
from app.ui.booking_form import BookingForm


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hospital Appointment System")
        self.root.geometry("600x400")

        tk.Label(
            self.root,
            text="Hospital Appointment System",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Admin Dashboard",
            width=25,
            command=self.open_admin
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Book Appointment",
            width=25,
            command=self.open_booking
        ).pack(pady=10)

    def open_admin(self):
        AdminDashboard(self.root)

    def open_booking(self):
        BookingForm(self.root)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()