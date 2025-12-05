import tkinter as tk
from tkinter import ttk, messagebox
from DB.db import get_connection

class TreatmentsScreen:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Treatments", font=("Arial", 18)).pack(pady=10)

        form = tk.Frame(self.frame)
        form.pack()

        tk.Label(form, text="Name: ").grid(row=0, column=0)
        tk.Label(form, text="Cost: ").grid(row=1, column=0)

        self.name = tk.Entry(form)
        self.cost = tk.Entry(form)

        self.name.grid(row=0, column=1)
        self.cost.grid(row=1, column=1)

        tk.Button(form, text="Add Treatment", command=self.add_treatment).grid(row=2, column=0, columnspan=2, pady=5)

        self.table = ttk.Treeview(self.frame, columns=("id", "name", "cost"), show="headings")
        self.table.pack(fill="both", expand=True, pady=10)

        for col in ("id", "name", "cost"):
            self.table.heading(col, text=col)

        tk.Button(self.frame, text="Delete Selected", command=self.delete_treatment).pack()

        self.load_data()

    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT treatment_id, name, cost FROM treatments")
        for row in cur.fetchall():
            self.table.insert("", "end", values=row)
        conn.close()

    def add_treatment(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO treatments (name, cost) VALUES (%s, %s)",
                    (self.name.get(), self.cost.get()))
        conn.commit()
        conn.close()
        self.load_data()
        messagebox.showinfo("Success", "Treatment added")

    def delete_treatment(self):
        selected = self.table.selection()
        if not selected:
            return
        treatment_id = self.table.item(selected[0])["values"][0]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM treatments WHERE treatment_id=%s", (treatment_id,))
        conn.commit()
        conn.close()
        self.load_data()
        messagebox.showinfo("Deleted", "Treatment removed")
