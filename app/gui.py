# hospital_app.py
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime

# ---------- CONFIG - update these to match your MySQL server ----------
db_config = {
    "host": "localhost",
    "user": "root",
    "passwd": "1234",           # <-- change if your MySQL has a password
    "database": "hospital"  # database created by the SQL script you ran
}

# ---------- APP ----------
class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        self.root.geometry(f"{int(w*0.85)}x{int(h*0.80)}+20+20")

        title = tk.Label(self.root, text="Hospital Management System",
                         font=("Arial", 20, "bold"), bd=2, relief="groove", pady=6)
        title.pack(fill="x")

        nav = tk.Frame(self.root)
        nav.pack(fill="x", pady=6)

        tk.Button(nav, text="Patients", width=14, command=self.show_patients).pack(side="left", padx=6)
        tk.Button(nav, text="Doctors", width=14, command=self.show_doctors).pack(side="left", padx=6)
        tk.Button(nav, text="Treatments", width=14, command=self.show_treatments).pack(side="left", padx=6)
        tk.Button(nav, text="Sessions", width=14, command=self.show_sessions).pack(side="left", padx=6)

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True, padx=8, pady=8)

        # Ensure tables exist (safe even if you already created them)
        try:
            self.ensure_tables()
        except Exception as e:
            messagebox.showerror("DB Error", f"Could not ensure tables: {e}")

        # Start with Patients screen
        self.show_patients()
    def search_entities(self, table, search_value):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if table == "patients":
                query = """
                    SELECT id, name, birthdate 
                    FROM patients
                    WHERE id LIKE %s OR name LIKE %s
                """

            elif table == "doctors":
                query = """
                    SELECT id, name, specialty
                    FROM doctors
                    WHERE id LIKE %s OR name LIKE %s
                """

            elif table == "treatments":
                query = """
                    SELECT id, name, cost
                    FROM treatments
                    WHERE id LIKE %s OR name LIKE %s
                """

            elif table == "sessions":
                query = """
                    SELECT sessions.id, sessions.name, patients.name, doctors.name, sessions.treatment_date
                    FROM sessions
                    JOIN patients ON patients.id = sessions.patient_id
                    JOIN doctors ON doctors.id = sessions.doctor_id
                    WHERE sessions.id LIKE %s
                    OR sessions.name LIKE %s
                    OR patients.name LIKE %s
                    OR doctors.name LIKE %s
                """
                cursor.execute(query, (f"%{search_value}%", f"%{search_value}%", f"%{search_value}%", f"%{search_value}%"))
                rows = cursor.fetchall()
                return rows

            cursor.execute(query, (f"%{search_value}%", f"%{search_value}%"))
            rows = cursor.fetchall()
            return rows

        except Exception as e:
            messagebox.showerror("DB Error", f"Error searching: {e}")
            return []

        finally:
            if conn:
                conn.close()  ## UI elements and methods

    # ---------- DB helpers ----------
    def db_connect(self):
        return pymysql.connect(host=db_config["host"],
                               user=db_config["user"],
                               passwd=db_config["passwd"],
                               database=db_config["database"],
                               cursorclass=pymysql.cursors.Cursor)

    def ensure_tables(self):
        con = self.db_connect()
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100),
                specialty VARCHAR(100)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100),
                birthdate DATE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS treatments (
                treatment_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100),
                cost DECIMAL(10,2)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id INT PRIMARY KEY AUTO_INCREMENT,
                patient_id INT,
                doctor_id INT,
                treatment_id INT,
                treatment_date DATE,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE SET NULL ON UPDATE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE SET NULL ON UPDATE CASCADE,
                FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id) ON DELETE SET NULL ON UPDATE CASCADE
            )
        """)
        con.commit()
        con.close()

    # ---------- Utilities ----------
    def clear_container(self):
        for w in self.container.winfo_children():
            w.destroy()

    def parse_date(self, s):
        """Expect YYYY-MM-DD. Return date string or raise ValueError."""
        try:
            dt = datetime.strptime(s, "%Y-%m-%d")
            return dt.date().isoformat()
        except Exception:
            raise ValueError("Date must be in YYYY-MM-DD format")

    # ---------- PATIENTS ----------
    def show_patients(self):
        self.clear_container()
        frame = tk.Frame(self.container, padx=8, pady=8)
        frame.pack(fill="both", expand=True)

        left = tk.Frame(frame)
        left.pack(side="left", fill="y", padx=8)

        tk.Label(left, text="Patient ID (blank for new):").grid(row=0, column=0, sticky="w", pady=6)
        self.p_id = tk.Entry(left); self.p_id.grid(row=0, column=1, pady=6)

        tk.Label(left, text="Name:").grid(row=1, column=0, sticky="w", pady=6)
        self.p_name = tk.Entry(left); self.p_name.grid(row=1, column=1, pady=6)

        tk.Label(left, text="Birthdate (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", pady=6)
        self.p_bdate = tk.Entry(left); self.p_bdate.grid(row=2, column=1, pady=6)

        bf = tk.Frame(left); bf.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(bf, text="Add", width=10, command=self.add_patient).pack(side="left", padx=4)
        tk.Button(bf, text="Update", width=10, command=self.update_patient).pack(side="left", padx=4)
        tk.Button(bf, text="Delete Selected", width=14, command=self.delete_patient_selected).pack(side="left", padx=4)
        tk.Button(bf, text="Clear", width=10, command=self.clear_patient_fields).pack(side="left", padx=4)
        tk.Button(bf, text="Refresh", width=10, command=self.load_patients).pack(side="left", padx=4)

        right = tk.Frame(frame)
        right.pack(side="right", fill="both", expand=True, padx=8)

        cols = ("patient_id", "name", "birthdate")
        self.p_table = ttk.Treeview(right, columns=cols, show="headings")
        for c in cols:
            self.p_table.heading(c, text=c.replace("_", " ").title())
            self.p_table.column(c, anchor="w", width=150)
        self.p_table.pack(fill="both", expand=True, side="left")
        scr = ttk.Scrollbar(right, orient="vertical", command=self.p_table.yview); self.p_table.configure(yscroll=scr.set); scr.pack(side="right", fill="y")
        self.p_table.bind("<Double-1>", self.on_patient_double)

        self.load_patients()

    def load_patients(self):
        for r in self.p_table.get_children(): self.p_table.delete(r)
        try:
            con = self.db_connect(); cur = con.cursor()
            cur.execute("SELECT patient_id, name, birthdate FROM patients ORDER BY patient_id")
            for row in cur.fetchall():
                bdate = row[2].isoformat() if row[2] is not None else ""
                self.p_table.insert("", "end", values=(row[0], row[1], bdate))
            con.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_patient(self):
        name = self.p_name.get().strip()
        bdate = self.p_bdate.get().strip()
        if not name:
            messagebox.showerror("Error", "Name required"); return
        try:
            bdate_val = self.parse_date(bdate) if bdate else None
            con = self.db_connect(); cur = con.cursor()
            if bdate_val:
                cur.execute("INSERT INTO patients (name, birthdate) VALUES (%s,%s)", (name, bdate_val))
            else:
                cur.execute("INSERT INTO patients (name) VALUES (%s)", (name,))
            con.commit(); con.close()
            messagebox.showinfo("Success", "Patient added")
            self.clear_patient_fields(); self.load_patients()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_patient(self):
        pid = self.p_id.get().strip()
        if not pid:
            messagebox.showerror("Error", "Enter patient ID (or double-click a row)."); return
        name = self.p_name.get().strip(); bdate = self.p_bdate.get().strip()
        if not name:
            messagebox.showerror("Error", "Name required"); return
        try:
            bdate_val = self.parse_date(bdate) if bdate else None
            con = self.db_connect(); cur = con.cursor()
            if bdate_val:
                cur.execute("UPDATE patients SET name=%s, birthdate=%s WHERE patient_id=%s", (name, bdate_val, int(pid)))
            else:
                cur.execute("UPDATE patients SET name=%s, birthdate=NULL WHERE patient_id=%s", (name, int(pid)))
            con.commit(); con.close()
            messagebox.showinfo("Success", f"Patient {pid} updated")
            self.load_patients()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_patient_selected(self):
        sel = self.p_table.selection()
        if not sel:
            messagebox.showerror("Error", "Select a patient row first."); return
        vals = self.p_table.item(sel[0], "values"); pid = vals[0]
        if messagebox.askyesno("Confirm", f"Delete patient {pid}?"):
            try:
                con = self.db_connect(); cur = con.cursor()
                cur.execute("DELETE FROM patients WHERE patient_id=%s", (int(pid),))
                con.commit(); con.close()
                messagebox.showinfo("Deleted", f"Patient {pid} deleted")
                self.load_patients()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_patient_double(self, event):
        sel = self.p_table.selection()
        if not sel: return
        vals = self.p_table.item(sel[0], "values")
        self.p_id.delete(0, tk.END); self.p_id.insert(0, vals[0])
        self.p_name.delete(0, tk.END); self.p_name.insert(0, vals[1])
        self.p_bdate.delete(0, tk.END); self.p_bdate.insert(0, vals[2] if vals[2] else "")

    def clear_patient_fields(self):
        self.p_id.delete(0, tk.END); self.p_name.delete(0, tk.END); self.p_bdate.delete(0, tk.END)

    # ---------- DOCTORS ----------
    def show_doctors(self):
        self.clear_container()
        frame = tk.Frame(self.container, padx=8, pady=8); frame.pack(fill="both", expand=True)
        left = tk.Frame(frame); left.pack(side="left", fill="y", padx=8)

        tk.Label(left, text="Doctor ID (blank for new):").grid(row=0, column=0, sticky="w", pady=6)
        self.d_id = tk.Entry(left); self.d_id.grid(row=0, column=1, pady=6)

        tk.Label(left, text="Name:").grid(row=1, column=0, sticky="w", pady=6)
        self.d_name = tk.Entry(left); self.d_name.grid(row=1, column=1, pady=6)

        tk.Label(left, text="Specialty:").grid(row=2, column=0, sticky="w", pady=6)
        self.d_spec = tk.Entry(left); self.d_spec.grid(row=2, column=1, pady=6)

        bf = tk.Frame(left); bf.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(bf, text="Add", width=10, command=self.add_doctor).pack(side="left", padx=4)
        tk.Button(bf, text="Update", width=10, command=self.update_doctor).pack(side="left", padx=4)
        tk.Button(bf, text="Delete Selected", width=14, command=self.delete_doctor_selected).pack(side="left", padx=4)
        tk.Button(bf, text="Clear", width=10, command=self.clear_doctor_fields).pack(side="left", padx=4)
        tk.Button(bf, text="Refresh", width=10, command=self.load_doctors).pack(side="left", padx=4)

        right = tk.Frame(frame); right.pack(side="right", fill="both", expand=True, padx=8)
        cols = ("doctor_id", "name", "specialty")
        self.d_table = ttk.Treeview(right, columns=cols, show="headings")
        for c in cols:
            self.d_table.heading(c, text=c.replace("_", " ").title())
            self.d_table.column(c, anchor="w", width=160)
        self.d_table.pack(fill="both", expand=True, side="left")
        sd = ttk.Scrollbar(right, orient="vertical", command=self.d_table.yview); self.d_table.configure(yscroll=sd.set); sd.pack(side="right", fill="y")
        self.d_table.bind("<Double-1>", self.on_doctor_double)

        self.load_doctors()

    def load_doctors(self):
        for r in self.d_table.get_children(): self.d_table.delete(r)
        try:
            con = self.db_connect(); cur = con.cursor()
            cur.execute("SELECT doctor_id, name, specialty FROM doctors ORDER BY doctor_id")
            for row in cur.fetchall():
                self.d_table.insert("", "end", values=row)
            con.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_doctor(self):
        name = self.d_name.get().strip(); spec = self.d_spec.get().strip()
        if not name: messagebox.showerror("Error", "Name required"); return
        try:
            con = self.db_connect(); cur = con.cursor()
            cur.execute("INSERT INTO doctors (name, specialty) VALUES (%s,%s)", (name, spec))
            con.commit(); con.close()
            messagebox.showinfo("Success", "Doctor added"); self.clear_doctor_fields(); self.load_doctors()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_doctor(self):
        did = self.d_id.get().strip()
        if not did: messagebox.showerror("Error", "Enter doctor ID"); return
        name = self.d_name.get().strip(); spec = self.d_spec.get().strip()
        if not name: messagebox.showerror("Error", "Name required"); return
        try:
            con = self.db_connect(); cur = con.cursor()
            cur.execute("UPDATE doctors SET name=%s, specialty=%s WHERE doctor_id=%s", (name, spec, int(did)))
            con.commit(); con.close()
            messagebox.showinfo("Success", f"Doctor {did} updated"); self.load_doctors()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_doctor_selected(self):
        sel = self.d_table.selection()
        if not sel: messagebox.showerror("Error", "Select doctor row first"); return
        vals = self.d_table.item(sel[0], "values"); did = vals[0]
        if messagebox.askyesno("Confirm", f"Delete doctor {did}? Sessions will set doctor_id NULL."):
            try:
                con = self.db_connect(); cur = con.cursor()
                cur.execute("DELETE FROM doctors WHERE doctor_id=%s", (int(did),))
                con.commit(); con.close()
                messagebox.showinfo("Deleted", f"Doctor {did} deleted"); self.load_doctors()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_doctor_double(self, event):
        sel = self.d_table.selection()
        if not sel: return
        vals = self.d_table.item(sel[0], "values")
        self.d_id.delete(0, tk.END); self.d_id.insert(0, vals[0])
        self.d_name.delete(0, tk.END); self.d_name.insert(0, vals[1])
        self.d_spec.delete(0, tk.END); self.d_spec.insert(0, vals[2])

    def clear_doctor_fields(self):
        self.d_id.delete(0, tk.END); self.d_name.delete(0, tk.END); self.d_spec.delete(0, tk.END)

    # ---------- TREATMENTS ----------
    def show_treatments(self):
        self.clear_container()
        frame = tk.Frame(self.container, padx=8, pady=8); frame.pack(fill="both", expand=True)
        left = tk.Frame(frame); left.pack(side="left", fill="y", padx=8)

        tk.Label(left, text="Treatment ID (blank for new):").grid(row=0, column=0, sticky="w", pady=6)
        self.t_id = tk.Entry(left); self.t_id.grid(row=0, column=1, pady=6)

        tk.Label(left, text="Name:").grid(row=1, column=0, sticky="w", pady=6)
        self.t_name = tk.Entry(left); self.t_name.grid(row=1, column=1, pady=6)

        tk.Label(left, text="Cost (e.g. 150.00):").grid(row=2, column=0, sticky="w", pady=6)
        self.t_cost = tk.Entry(left); self.t_cost.grid(row=2, column=1, pady=6)

        bf = tk.Frame(left); bf.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(bf, text="Add", width=10, command=self.add_treatment).pack(side="left", padx=4)
        tk.Button(bf, text="Update", width=10, command=self.update_treatment).pack(side="left", padx=4)
        tk.Button(bf, text="Delete Selected", width=14, command=self.delete_treatment_selected).pack(side="left", padx=4)
        tk.Button(bf, text="Clear", width=10, command=self.clear_treatment_fields).pack(side="left", padx=4)
        tk.Button(bf, text="Refresh", width=10, command=self.load_treatments).pack(side="left", padx=4)

        right = tk.Frame(frame); right.pack(side="right", fill="both", expand=True, padx=8)
        cols = ("treatment_id", "name", "cost")
        self.t_table = ttk.Treeview(right, columns=cols, show="headings")
        for c in cols:
            self.t_table.heading(c, text=c.replace("_", " ").title())
            self.t_table.column(c, anchor="w", width=150)
        self.t_table.pack(fill="both", expand=True, side="left")
        st = ttk.Scrollbar(right, orient="vertical", command=self.t_table.yview); self.t_table.configure(yscroll=st.set); st.pack(side="right", fill="y")
        self.t_table.bind("<Double-1>", self.on_treatment_double)

        self.load_treatments()

    def load_treatments(self):
        for r in self.t_table.get_children(): self.t_table.delete(r)
        try:
            con = self.db_connect(); cur = con.cursor()
            cur.execute("SELECT treatment_id, name, cost FROM treatments ORDER BY treatment_id")
            for row in cur.fetchall():
                self.t_table.insert("", "end", values=(row[0], row[1], float(row[2]) if row[2] is not None else 0.0))
            con.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_treatment(self):
        name = self.t_name.get().strip(); cost = self.t_cost.get().strip()
        if not name: messagebox.showerror("Error", "Name required"); return
        try:
            cost_val = float(cost) if cost else 0.0
            con = self.db_connect(); cur = con.cursor()
            cur.execute("INSERT INTO treatments (name, cost) VALUES (%s,%s)", (name, cost_val))
            con.commit(); con.close()
            messagebox.showinfo("Success", "Treatment added"); self.clear_treatment_fields(); self.load_treatments()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_treatment(self):
        tid = self.t_id.get().strip()
        if not tid: messagebox.showerror("Error", "Enter treatment ID"); return
        name = self.t_name.get().strip(); cost = self.t_cost.get().strip()
        if not name: messagebox.showerror("Error", "Name required"); return
        try:
            cost_val = float(cost) if cost else 0.0
            con = self.db_connect(); cur = con.cursor()
            cur.execute("UPDATE treatments SET name=%s, cost=%s WHERE treatment_id=%s", (name, cost_val, int(tid)))
            con.commit(); con.close()
            messagebox.showinfo("Success", f"Treatment {tid} updated"); self.load_treatments()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_treatment_selected(self):
        sel = self.t_table.selection()
        if not sel: messagebox.showerror("Error", "Select treatment row first"); return
        vals = self.t_table.item(sel[0], "values"); tid = vals[0]
        if messagebox.askyesno("Confirm", f"Delete treatment {tid}? Sessions will set treatment_id NULL."):
            try:
                con = self.db_connect(); cur = con.cursor()
                cur.execute("DELETE FROM treatments WHERE treatment_id=%s", (int(tid),))
                con.commit(); con.close()
                messagebox.showinfo("Deleted", f"Treatment {tid} deleted"); self.load_treatments()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_treatment_double(self, event):
        sel = self.t_table.selection()
        if not sel: return
        vals = self.t_table.item(sel[0], "values")
        self.t_id.delete(0, tk.END); self.t_id.insert(0, vals[0])
        self.t_name.delete(0, tk.END); self.t_name.insert(0, vals[1])
        self.t_cost.delete(0, tk.END); self.t_cost.insert(0, str(vals[2]))

    def clear_treatment_fields(self):
        self.t_id.delete(0, tk.END); self.t_name.delete(0, tk.END); self.t_cost.delete(0, tk.END)

    # ---------- SESSIONS ----------
    def show_sessions(self):
        self.clear_container()
        frame = tk.Frame(self.container, padx=8, pady=8); frame.pack(fill="both", expand=True)
        left = tk.Frame(frame); left.pack(side="left", fill="y", padx=8)

        tk.Label(left, text="Session ID (blank for new):").grid(row=0, column=0, sticky="w", pady=6)
        self.s_id = tk.Entry(left); self.s_id.grid(row=0, column=1, pady=6)

        tk.Label(left, text="Patient:").grid(row=1, column=0, sticky="w", pady=6)
        self.s_patient_var = tk.StringVar(); self.s_patient_cb = ttk.Combobox(left, textvariable=self.s_patient_var, state="readonly"); self.s_patient_cb.grid(row=1, column=1, pady=6)

        tk.Label(left, text="Doctor:").grid(row=2, column=0, sticky="w", pady=6)
        self.s_doctor_var = tk.StringVar(); self.s_doctor_cb = ttk.Combobox(left, textvariable=self.s_doctor_var, state="readonly"); self.s_doctor_cb.grid(row=2, column=1, pady=6)

        tk.Label(left, text="Treatment:").grid(row=3, column=0, sticky="w", pady=6)
        self.s_treatment_var = tk.StringVar(); self.s_treatment_cb = ttk.Combobox(left, textvariable=self.s_treatment_var, state="readonly"); self.s_treatment_cb.grid(row=3, column=1, pady=6)

        tk.Label(left, text="Date (YYYY-MM-DD):").grid(row=4, column=0, sticky="w", pady=6)
        self.s_date = tk.Entry(left); self.s_date.grid(row=4, column=1, pady=6)

        bf = tk.Frame(left); bf.grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(bf, text="Add", width=10, command=self.add_session).pack(side="left", padx=4)
        tk.Button(bf, text="Update", width=10, command=self.update_session).pack(side="left", padx=4)
        tk.Button(bf, text="Delete Selected", width=14, command=self.delete_session_selected).pack(side="left", padx=4)
        tk.Button(bf, text="Clear", width=10, command=self.clear_session_fields).pack(side="left", padx=4)
        tk.Button(bf, text="Refresh", width=10, command=self.load_sessions).pack(side="left", padx=4)

        right = tk.Frame(frame); right.pack(side="right", fill="both", expand=True, padx=8)
        cols = ("session_id", "patient", "doctor", "treatment", "treatment_date")
        self.s_table = ttk.Treeview(right, columns=cols, show="headings")
        for c in cols:
            self.s_table.heading(c, text=c.replace("_", " ").title())
            self.s_table.column(c, anchor="w", width=140)
        self.s_table.pack(fill="both", expand=True, side="left")
        ss = ttk.Scrollbar(right, orient="vertical", command=self.s_table.yview); self.s_table.configure(yscroll=ss.set); ss.pack(side="right", fill="y")
        self.s_table.bind("<Double-1>", self.on_session_double)

        self.load_sessions_dropdowns(); self.load_sessions()

    def load_sessions_dropdowns(self):
        try:
            con = self.db_connect(); cur = con.cursor()
            cur.execute("SELECT patient_id, name FROM patients ORDER BY patient_id")
            pvals = [f"{r[0]}: {r[1]}" for r in cur.fetchall()]
            self.s_patient_cb["values"] = pvals

            cur.execute("SELECT doctor_id, name FROM doctors ORDER BY doctor_id")
            dvals = [f"{r[0]}: {r[1]}" for r in cur.fetchall()]
            self.s_doctor_cb["values"] = dvals

            cur.execute("SELECT treatment_id, name FROM treatments ORDER BY treatment_id")
            tvals = [f"{r[0]}: {r[1]}" for r in cur.fetchall()]
            self.s_treatment_cb["values"] = tvals
            con.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_sessions(self):
        for r in self.s_table.get_children(): self.s_table.delete(r)
        try:
            con = self.db_connect(); cur = con.cursor()
            cur.execute("""
                SELECT s.session_id,
                       p.patient_id, p.name,
                       d.doctor_id, d.name,
                       t.treatment_id, t.name,
                       s.treatment_date
                FROM sessions s
                LEFT JOIN patients p ON s.patient_id = p.patient_id
                LEFT JOIN doctors d ON s.doctor_id = d.doctor_id
                LEFT JOIN treatments t ON s.treatment_id = t.treatment_id
                ORDER BY s.session_id
            """)
            for row in cur.fetchall():
                sid = row[0]
                patient_display = f"{row[1]}: {row[2]}" if row[1] else ""
                doctor_display = f"{row[3]}: {row[4]}" if row[3] else ""
                treat_display = f"{row[5]}: {row[6]}" if row[5] else ""
                tdate = row[7].isoformat() if row[7] is not None else ""
                self.s_table.insert("", "end", values=(sid, patient_display, doctor_display, treat_display, tdate))
            con.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_session(self):
        p = self.s_patient_var.get(); d = self.s_doctor_var.get(); t = self.s_treatment_var.get(); date_s = self.s_date.get().strip()
        if not p or not d or not t:
            messagebox.showerror("Error", "Select patient, doctor and treatment"); return
        try:
            date_val = self.parse_date(date_s)
        except Exception as e:
            messagebox.showerror("Error", str(e)); return
        pid = int(p.split(":")[0]); did = int(d.split(":")[0]); tid = int(t.split(":")[0])
        try:
            con = self.db_connect(); cur = con.cursor()
            cur.execute("INSERT INTO sessions (patient_id, doctor_id, treatment_id, treatment_date) VALUES (%s,%s,%s,%s)",
                        (pid, did, tid, date_val))
            con.commit(); con.close()
            messagebox.showinfo("Success", "Session added"); self.clear_session_fields(); self.load_sessions()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_session(self):
        sid = self.s_id.get().strip()
        if not sid: messagebox.showerror("Error", "Enter session ID or double-click a row"); return
        p = self.s_patient_var.get(); d = self.s_doctor_var.get(); t = self.s_treatment_var.get(); date_s = self.s_date.get().strip()
        if not p or not d or not t:
            messagebox.showerror("Error", "Select patient, doctor and treatment"); return
        try:
            date_val = self.parse_date(date_s)
        except Exception as e:
            messagebox.showerror("Error", str(e)); return
        pid = int(p.split(":")[0]); did = int(d.split(":")[0]); tid = int(t.split(":")[0])
        try:
            con = self.db_connect(); cur = con.cursor()
            cur.execute("UPDATE sessions SET patient_id=%s, doctor_id=%s, treatment_id=%s, treatment_date=%s WHERE session_id=%s",
                        (pid, did, tid, date_val, int(sid)))
            con.commit(); con.close()
            messagebox.showinfo("Success", f"Session {sid} updated"); self.load_sessions(); self.clear_session_fields()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_session_selected(self):
        sel = self.s_table.selection()
        if not sel: messagebox.showerror("Error", "Select session row first"); return
        vals = self.s_table.item(sel[0], "values"); sid = vals[0]
        if messagebox.askyesno("Confirm", f"Delete session {sid}?"):
            try:
                con = self.db_connect(); cur = con.cursor()
                cur.execute("DELETE FROM sessions WHERE session_id=%s", (int(sid),))
                con.commit(); con.close()
                messagebox.showinfo("Deleted", f"Session {sid} deleted"); self.load_sessions()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_session_double(self, event):
        sel = self.s_table.selection()
        if not sel: return
        vals = self.s_table.item(sel[0], "values")
        sid = vals[0]
        self.s_id.delete(0, tk.END); self.s_id.insert(0, sid)
        self.s_patient_var.set(vals[1]); self.s_doctor_var.set(vals[2]); self.s_treatment_var.set(vals[3])
        self.s_date.delete(0, tk.END); self.s_date.insert(0, vals[4] if vals[4] else "")

    def clear_session_fields(self):
        self.s_id.delete(0, tk.END); self.s_patient_var.set(""); self.s_doctor_var.set(""); self.s_treatment_var.set(""); self.s_date.delete(0, tk.END)

# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()
