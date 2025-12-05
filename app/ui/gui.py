import tkinter as tk
from tkinter import ttk
from services import patients, doctors, treatments, sessions

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.create_patient_screen()
        self.create_doctor_screen()
        self.create_treatment_screen()
        self.create_session_screen()

    def create_table(self, parent, data):
        tree = ttk.Treeview(parent, columns=list(data[0].keys()), show="headings")
        for col in data[0].keys():
            tree.heading(col, text=col)
            tree.column(col, width=120)
        for row in data:
            tree.insert("", tk.END, values=list(row.values()))
        tree.pack(fill="both", expand=True)

    def create_patient_screen(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Patients")
        data = patients.list_patients()
        if data:
            self.create_table(frame, data)

    def create_doctor_screen(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Doctors")
        data = doctors.get_all_doctors()
        if data:
            self.create_table(frame, data)

    def create_treatment_screen(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Treatments")
        data = treatments.get_all_treatments()
        if data:
            self.create_table(frame, data)

    def create_session_screen(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Sessions")
        data = sessions.get_all_sessions()
        if data:
            self.create_table(frame, data)
