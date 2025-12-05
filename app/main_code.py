import tkinter as tk
from app.patients_screen import PatientsScreen
from app.doctors_screen import DoctorsScreen
from app.treatments_screen import TreatmentsScreen
from app.sessions_screen import SessionsScreen

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1100x700")

        # Navigation buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(side="top", fill="x")

        tk.Button(btn_frame, text="Patients", width=20,
                  command=self.open_patients).pack(side="left")
        tk.Button(btn_frame, text="Doctors", width=20,
                  command=self.open_doctors).pack(side="left")
        tk.Button(btn_frame, text="Treatments", width=20,
                  command=self.open_treatments).pack(side="left")
        tk.Button(btn_frame, text="Sessions", width=20,
                  command=self.open_sessions).pack(side="left")

        self.screen_frame = tk.Frame(root)
        self.screen_frame.pack(fill="both", expand=True)

    def clear_screen(self):
        for widget in self.screen_frame.winfo_children():
            widget.destroy()

    def open_patients(self):
        self.clear_screen()
        PatientsScreen(self.screen_frame)

    def open_doctors(self):
        self.clear_screen()
        DoctorsScreen(self.screen_frame)

    def open_treatments(self):
        self.clear_screen()
        TreatmentsScreen(self.screen_frame)

    def open_sessions(self):
        self.clear_screen()
        SessionsScreen(self.screen_frame)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
