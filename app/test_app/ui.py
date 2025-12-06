# ui.py
import tkinter as tk
from tkinter import ttk, messagebox
import services as s

class HospitalApp:
    def __init__(self, root):
        self.root = root
        root.title("Hospital Management System")
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{int(w*0.85)}x{int(h*0.80)}+20+20")
        
        tk.Label(root, text="Hospital Management System", font=("Arial", 20, "bold"), bd=2, relief="groove", pady=6).pack(fill="x")
        nav = tk.Frame(root); nav.pack(fill="x", pady=6)
        
        btns = [("Patients", self.show_patients), ("Doctors", self.show_doctors),
                ("Treatments", self.show_treatments), ("Sessions", self.show_sessions)]
        for text, cmd in btns:
            tk.Button(nav, text=text, width=14, command=cmd).pack(side="left", padx=6)

        self.container = tk.Frame(root); self.container.pack(fill="both", expand=True, padx=8, pady=8)
        s.ensure_tables()
        self.show_patients()

    def clear_container(self):
        for w in self.container.winfo_children(): w.destroy()

    def setup_base_screen(self, title, fields, callbacks, cols, double_click_handler, load_func):
        self.clear_container()
        frame = tk.Frame(self.container, padx=8, pady=8); frame.pack(fill="both", expand=True)
        left = tk.Frame(frame); left.pack(side="left", fill="y", padx=8)

        # Input Fields Setup
        self.fields = {}
        row = 0
        for label_text, var_name, entry_cls, *extra in fields:
            tk.Label(left, text=label_text).grid(row=row, column=0, sticky="w", pady=6)
            if entry_cls == tk.Entry:
                self.fields[var_name] = tk.Entry(left)
                self.fields[var_name].grid(row=row, column=1, pady=6)
            elif entry_cls == ttk.Combobox:
                self.fields[f'{var_name}_var'] = tk.StringVar()
                cb = ttk.Combobox(left, textvariable=self.fields[f'{var_name}_var'], state="readonly", values=extra[0])
                cb.grid(row=row, column=1, pady=6)
                self.fields[var_name] = cb
            row += 1

        # Buttons Setup
        bf = tk.Frame(left); bf.grid(row=row, column=0, columnspan=2, pady=10)
        for text, cmd in callbacks:
            tk.Button(bf, text=text, width=14 if text == "Delete Selected" else 10, command=cmd).pack(side="left", padx=4)

        # Table Setup
        right = tk.Frame(frame); right.pack(side="right", fill="both", expand=True, padx=8)
        self.tree = ttk.Treeview(right, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, anchor="w", width=140 if len(cols) == 5 else 160)
        self.tree.pack(fill="both", expand=True, side="left")
        scr = ttk.Scrollbar(right, orient="vertical", command=self.tree.yview); self.tree.configure(yscroll=scr.set); scr.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", double_click_handler)
        
        load_func()

    # --- Patient Screen (P) ---
    def show_patients(self):
        fields = [
            ("Patient ID (blank for new):", 'p_id', tk.Entry),
            ("Name:", 'p_name', tk.Entry),
            ("Birthdate (YYYY-MM-DD):", 'p_bdate', tk.Entry)
        ]
        callbacks = [
            ("Add", self._p_add), ("Update", self._p_update),
            ("Delete Selected", self._p_delete), ("Clear", self.clear_patient_fields),
            ("Refresh", self.load_patients)
        ]
        self.setup_base_screen("Patients", fields, callbacks, ("id", "name", "birthdate"), self.on_patient_double, self.load_patients)
        self.p_fields = self.fields 

    def load_patients(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        for row in s.load_entities("patients"):
            bdate = row[2].isoformat() if row[2] else ""
            self.tree.insert("", "end", values=(row[0], row[1], bdate))

    def clear_patient_fields(self):
        for k in self.p_fields: self.p_fields[k].delete(0, tk.END)

    def _p_add(self):
        name = self.p_fields['p_name'].get().strip(); bdate = self.p_fields['p_bdate'].get().strip()
        if not name: messagebox.showerror("Error", "Name required"); return
        try: s.add_patient(name, bdate); messagebox.showinfo("Success", "Patient added"); self.clear_patient_fields(); self.load_patients()
        except Exception as e: messagebox.showerror("Error", str(e))
    
    def _p_update(self):
        pid = self.p_fields['p_id'].get().strip()
        if not pid: messagebox.showerror("Error", "Enter patient ID (or double-click a row)."); return
        name = self.p_fields['p_name'].get().strip(); bdate = self.p_fields['p_bdate'].get().strip()
        if not name: messagebox.showerror("Error", "Name required"); return
        try: s.update_patient(pid, name, bdate); messagebox.showinfo("Success", f"Patient {pid} updated"); self.load_patients()
        except Exception as e: messagebox.showerror("Error", str(e))
        
    def _p_delete(self):
        sel = self.tree.selection()
        if not sel: messagebox.showerror("Error", "Select a patient row first."); return
        pid = self.tree.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirm", f"Delete patient {pid}?"):
            try: s.delete_entity("patients", pid); messagebox.showinfo("Deleted", f"Patient {pid} deleted"); self.load_patients()
            except Exception as e: messagebox.showerror("Error", str(e))

    def on_patient_double(self, event):
        sel = self.tree.selection(); 
        if not sel: return
        vals = self.tree.item(sel[0], "values")
        self.p_fields['p_id'].delete(0, tk.END); self.p_fields['p_id'].insert(0, vals[0])
        self.p_fields['p_name'].delete(0, tk.END); self.p_fields['p_name'].insert(0, vals[1])
        self.p_fields['p_bdate'].delete(0, tk.END); self.p_fields['p_bdate'].insert(0, vals[2])

    # --- Doctor Screen (D) ---
    def show_doctors(self):
        fields = [
            ("Doctor ID (blank for new):", 'd_id', tk.Entry),
            ("Name:", 'd_name', tk.Entry),
            ("Specialty:", 'd_spec', tk.Entry)
        ]
        callbacks = [
            ("Add", self._d_add), ("Update", self._d_update),
            ("Delete Selected", self._d_delete), ("Clear", self.clear_doctor_fields),
            ("Refresh", self.load_doctors)
        ]
        self.setup_base_screen("Doctors", fields, callbacks, ("id", "name", "specialty"), self.on_doctor_double, self.load_doctors)
        self.d_fields = self.fields

    def load_doctors(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        for row in s.load_entities("doctors"): self.tree.insert("", "end", values=row)

    def clear_doctor_fields(self):
        for k in self.d_fields: self.d_fields[k].delete(0, tk.END)

    def _d_add(self):
        name = self.d_fields['d_name'].get().strip(); spec = self.d_fields['d_spec'].get().strip()
        if not name: messagebox.showerror("Error", "Name required"); return
        try: s.add_doctor(name, spec); messagebox.showinfo("Success", "Doctor added"); self.clear_doctor_fields(); self.load_doctors()
        except Exception as e: messagebox.showerror("Error", str(e))
    
    def _d_update(self):
        did = self.d_fields['d_id'].get().strip()
        if not did: messagebox.showerror("Error", "Enter doctor ID"); return
        name = self.d_fields['d_name'].get().strip(); spec = self.d_fields['d_spec'].get().strip()
        if not name: messagebox.showerror("Error", "Name required"); return
        try: s.update_doctor(did, name, spec); messagebox.showinfo("Success", f"Doctor {did} updated"); self.load_doctors()
        except Exception as e: messagebox.showerror("Error", str(e))
        
    def _d_delete(self):
        sel = self.tree.selection()
        if not sel: messagebox.showerror("Error", "Select doctor row first"); return
        did = self.tree.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirm", f"Delete doctor {did}? Sessions will set doctor_id NULL."):
            try: s.delete_entity("doctors", did); messagebox.showinfo("Deleted", f"Doctor {did} deleted"); self.load_doctors()
            except Exception as e: messagebox.showerror("Error", str(e))

    def on_doctor_double(self, event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0], "values")
        self.d_fields['d_id'].delete(0, tk.END); self.d_fields['d_id'].insert(0, vals[0])
        self.d_fields['d_name'].delete(0, tk.END); self.d_fields['d_name'].insert(0, vals[1])
        self.d_fields['d_spec'].delete(0, tk.END); self.d_fields['d_spec'].insert(0, vals[2])

    # --- Treatment Screen (T) ---
    def show_treatments(self):
        fields = [
            ("Treatment ID (blank for new):", 't_id', tk.Entry),
            ("Name:", 't_name', tk.Entry),
            ("Cost (e.g. 150.00):", 't_cost', tk.Entry)
        ]
        callbacks = [
            ("Add", self._t_add), ("Update", self._t_update),
            ("Delete Selected", self._t_delete), ("Clear", self.clear_treatment_fields),
            ("Refresh", self.load_treatments)
        ]
        self.setup_base_screen("Treatments", fields, callbacks, ("id", "name", "cost"), self.on_treatment_double, self.load_treatments)
        self.t_fields = self.fields

    def load_treatments(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        for row in s.load_entities("treatments"):
            cost = float(row[2]) if row[2] else 0.0
            self.tree.insert("", "end", values=(row[0], row[1], cost))

    def clear_treatment_fields(self):
        for k in self.t_fields: self.t_fields[k].delete(0, tk.END)

    def _t_add(self):
        name = self.t_fields['t_name'].get().strip(); cost = self.t_fields['t_cost'].get().strip()
        if not name: messagebox.showerror("Error", "Name required"); return
        try: s.add_treatment(name, cost); messagebox.showinfo("Success", "Treatment added"); self.clear_treatment_fields(); self.load_treatments()
        except Exception as e: messagebox.showerror("Error", str(e))
    
    def _t_update(self):
        tid = self.t_fields['t_id'].get().strip()
        if not tid: messagebox.showerror("Error", "Enter treatment ID"); return
        name = self.t_fields['t_name'].get().strip(); cost = self.t_fields['t_cost'].get().strip()
        if not name: messagebox.showerror("Error", "Name required"); return
        try: s.update_treatment(tid, name, cost); messagebox.showinfo("Success", f"Treatment {tid} updated"); self.load_treatments()
        except Exception as e: messagebox.showerror("Error", str(e))
        
    def _t_delete(self):
        sel = self.tree.selection()
        if not sel: messagebox.showerror("Error", "Select treatment row first"); return
        tid = self.tree.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirm", f"Delete treatment {tid}? Sessions will set treatment_id NULL."):
            try: s.delete_entity("treatments", tid); messagebox.showinfo("Deleted", f"Treatment {tid} deleted"); self.load_treatments()
            except Exception as e: messagebox.showerror("Error", str(e))

    def on_treatment_double(self, event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0], "values")
        self.t_fields['t_id'].delete(0, tk.END); self.t_fields['t_id'].insert(0, vals[0])
        self.t_fields['t_name'].delete(0, tk.END); self.t_fields['t_name'].insert(0, vals[1])
        self.t_fields['t_cost'].delete(0, tk.END); self.t_fields['t_cost'].insert(0, str(vals[2]))

    # --- Session Screen (S) ---
    def show_sessions(self):
        p_vals, d_vals, t_vals = s.get_session_fk_data()
        fields = [
            ("Session ID (blank for new):", 's_id', tk.Entry),
            ("Patient:", 's_patient', ttk.Combobox, p_vals),
            ("Doctor:", 's_doctor', ttk.Combobox, d_vals),
            ("Treatment:", 's_treatment', ttk.Combobox, t_vals),
            ("Date (YYYY-MM-DD):", 's_date', tk.Entry)
        ]
        callbacks = [
            ("Add", self._s_add), ("Update", self._s_update),
            ("Delete Selected", self._s_delete), ("Clear", self.clear_session_fields),
            ("Refresh", self.load_sessions)
        ]
        self.setup_base_screen("Sessions", fields, callbacks, ("id", "patient", "doctor", "treatment", "date"), self.on_session_double, self.load_sessions)
        self.s_fields = self.fields

    def load_sessions(self):
        # Reload dropdowns on refresh as FK data might have changed
        p_vals, d_vals, t_vals = s.get_session_fk_data()
        self.s_fields['s_patient']["values"] = p_vals
        self.s_fields['s_doctor']["values"] = d_vals
        self.s_fields['s_treatment']["values"] = t_vals
        
        for r in self.tree.get_children(): self.tree.delete(r)
        for row in s.load_sessions_data():
            sid = row[0]
            patient_display = f"{row[1]}: {row[2]}" if row[1] else ""
            doctor_display = f"{row[3]}: {row[4]}" if row[3] else ""
            treat_display = f"{row[5]}: {row[6]}" if row[5] else ""
            tdate = row[7].isoformat() if row[7] else ""
            self.tree.insert("", "end", values=(sid, patient_display, doctor_display, treat_display, tdate))

    def clear_session_fields(self):
        self.s_fields['s_id'].delete(0, tk.END)
        self.s_fields['s_date'].delete(0, tk.END)
        self.s_fields['s_patient_var'].set("")
        self.s_fields['s_doctor_var'].set("")
        self.s_fields['s_treatment_var'].set("")

    def _s_add(self):
        p = self.s_fields['s_patient_var'].get(); d = self.s_fields['s_doctor_var'].get(); t = self.s_fields['s_treatment_var'].get(); date_s = self.s_fields['s_date'].get().strip()
        if not all([p, d, t, date_s]): messagebox.showerror("Error", "All fields required (Patient, Doctor, Treatment, Date)"); return
        try: s.add_session(p, d, t, date_s); messagebox.showinfo("Success", "Session added"); self.clear_session_fields(); self.load_sessions()
        except Exception as e: messagebox.showerror("Error", str(e))
    
    def _s_update(self):
        sid = self.s_fields['s_id'].get().strip()
        if not sid: messagebox.showerror("Error", "Enter session ID or double-click a row"); return
        p = self.s_fields['s_patient_var'].get(); d = self.s_fields['s_doctor_var'].get(); t = self.s_fields['s_treatment_var'].get(); date_s = self.s_fields['s_date'].get().strip()
        if not all([p, d, t, date_s]): messagebox.showerror("Error", "All fields required (Patient, Doctor, Treatment, Date)"); return
        try: s.update_session(sid, p, d, t, date_s); messagebox.showinfo("Success", f"Session {sid} updated"); self.load_sessions(); self.clear_session_fields()
        except Exception as e: messagebox.showerror("Error", str(e))

    def _s_delete(self):
        sel = self.tree.selection()
        if not sel: messagebox.showerror("Error", "Select session row first"); return
        sid = self.tree.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirm", f"Delete session {sid}?"):
            try: s.delete_entity("sessions", sid); messagebox.showinfo("Deleted", f"Session {sid} deleted"); self.load_sessions()
            except Exception as e: messagebox.showerror("Error", str(e))

    def on_session_double(self, event):
        sel = self.tree.selection(); 
        if not sel: return
        vals = self.tree.item(sel[0], "values")
        self.s_fields['s_id'].delete(0, tk.END); self.s_fields['s_id'].insert(0, vals[0])
        self.s_fields['s_patient_var'].set(vals[1]); self.s_fields['s_doctor_var'].set(vals[2]); self.s_fields['s_treatment_var'].set(vals[3])
        self.s_fields['s_date'].delete(0, tk.END); self.s_fields['s_date'].insert(0, vals[4])