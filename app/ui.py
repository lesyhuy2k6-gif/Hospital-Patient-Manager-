import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import decimal
import csv 
import services as s
import queries as q
from dashboard import DashboardTab 
import re

# --- Helper Functions ---

def fmt_date(v):
    """Formats a datetime object to a simple string, otherwise returns the value."""
    if isinstance(v, (datetime, date)):
        return v.strftime("%Y-%m-%d")
    return v

def parse_date_or_none(date_str):
    """Attempts to parse a date string (YYYY-MM-DD) or returns None/raises ValueError."""
    if not date_str:
        return None
    return datetime.strptime(date_str, "%Y-%m-%d").date()


class HospitalApp:
    def __init__(self, root):
        # --- COLOR THEME CONFIGURATION ---
        self.colors = {
            'bg_main': '#f0f0f0',        # Main background
            'bg_dark': '#2c3e50',        # Dark background (header)
            'bg_light': '#ecf0f1',       # Light background
            'text_dark': '#2c3e50',      # Dark text
            'text_light': '#ffffff',     # Light text
            'primary': '#3498db',        # Primary color (buttons)
            'success': '#27ae60',        # Success color (add button)
            'danger': '#e74c3c',         # Danger color (delete button)
            'warning': '#f39c12',        # Warning color
            'border': '#bdc3c7'          # Border color
        }
        
        # --- Root Setup ---
        self.root = root
        root.title("Hospital Management System")
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{int(w*0.85)}x{int(h*0.80)}+20+20")
        root.configure(bg=self.colors['bg_main'])
        
        # --- TTK STYLE CONFIGURATION ---
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles for ttk widgets
        style.configure('TLabel', background=self.colors['bg_main'], foreground=self.colors['text_dark'])
        style.configure('TFrame', background=self.colors['bg_main'])
        style.configure('TNotebook', background=self.colors['bg_main'])
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Arial', 10))
        style.map('TNotebook.Tab', background=[('selected', self.colors['primary'])])
        
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.map('TButton',
                  background=[('active', self.colors['primary']),
                              ('pressed', self.colors['bg_dark'])])
        
        # Configure Treeview style
        style.configure('Treeview', background=self.colors['bg_light'], 
                       foreground=self.colors['text_dark'], fieldbackground=self.colors['bg_light'],
                       font=('Arial', 9), rowheight=25)
        style.configure('Treeview.Heading', background=self.colors['primary'], 
                       foreground=self.colors['text_light'], font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', self.colors['primary'])])
        
        # --- Main Title ---
        tk.Label(root, text="Hospital Management System", font=("Arial", 20, "bold"), 
                bd=2, relief="groove", pady=6, bg=self.colors['bg_dark'], 
                fg=self.colors['text_light']).pack(fill="x")
        
        # --- Tab Navigation ---
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=1, fill="both")

        # --- Tab Definitions (7 tabs total) ---
        self.tab_patients = ttk.Frame(self.tabs); self.tabs.add(self.tab_patients, text="Patients")
        self.tab_doctors = ttk.Frame(self.tabs); self.tabs.add(self.tab_doctors, text="Doctors")
        self.tab_treatments = ttk.Frame(self.tabs); self.tabs.add(self.tab_treatments, text="Treatments")
        self.tab_sessions = ttk.Frame(self.tabs); self.tabs.add(self.tab_sessions, text="Sessions")

        # --- NEW Tabs ---
        self.tab_global_search = ttk.Frame(self.tabs); self.tabs.add(self.tab_global_search, text="Global Search")
        self.tab_reports = ttk.Frame(self.tabs); self.tabs.add(self.tab_reports, text="Reports")
        self.tab_dashboard = DashboardTab(self.tabs); self.tabs.add(self.tab_dashboard, text="Dashboard") 

        # --- UI State Variables ---
        self.g_search = tk.StringVar()
        self.g_search_tree = None
        self.report_tree = None
        
        s.ensure_tables() # Initialize DB tables
        self.build_patients_tab() 
        self.build_doctors_tab()
        self.build_treatments_tab()
        self.build_sessions_tab()
        self.build_global_search_tab()
        self.build_reports_tab() 
        
        self.tabs.select(self.tab_patients)

    # --- Reusable helper ---
    def clear_container(self, frame):
        for w in frame.winfo_children(): w.destroy()

    def _validate_alpha(self, proposed: str) -> bool:
        """Validate that the proposed value contains only letters, spaces, hyphens, periods, or apostrophes.
        Used as a `validatecommand` for Entry widgets. Empty string is allowed during editing.
        """
        if proposed is None or proposed == "":
            return True
        # CHANGE: Added '.' inside the character class to allow periods for names/titles like 'Dr. J. Doe'
        return bool(re.match(r"^[A-Za-z\s\-\.']*$", proposed))

    def _validate_phone_chars(self, proposed: str) -> bool:
        """Validate that the proposed value contains only digits, spaces, hyphens, plus signs, or parentheses.
        Used as a `validatecommand` for Entry widgets. Empty string is allowed during editing.
        """
        if proposed is None or proposed == "":
            return True
        # Allows 0-9, spaces, hyphens, plus sign, and parentheses
        return bool(re.match(r"^[0-9\s\-\+\(\)]*$", proposed))

    def _validate_cost_input(self, proposed: str) -> bool:
        """Validate that the proposed value is a valid non-negative decimal string (0-9 and one dot only).
        Empty string is allowed. Prevents invalid characters from being typed.
        """
        if proposed is None or proposed == "":
            return True
        # Check for non-negativity in this UI validator: must not start with '-'
        if proposed.startswith('-'):
            return False
        
        # Check if it matches a non-negative float format (e.g., 123, 123.00, .5, 0.5)
        # Using a strict regex that only allows one dot and digits
        return bool(re.match(r"^\d*\.?\d*$", proposed))
    
    def setup_base_screen(self, frame, fields, callbacks, cols, double_click_handler, load_func):
        self.clear_container(frame)
        
        base_frame = tk.Frame(frame, padx=8, pady=8); base_frame.pack(fill="both", expand=True)
        left = tk.Frame(base_frame); left.pack(side="left", fill="y", padx=8)

        # Input Fields Setup...
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

        # Buttons Setup...
        bf = tk.Frame(left); bf.grid(row=row, column=0, columnspan=2, pady=10)
        for text, cmd in callbacks:
            tk.Button(bf, text=text, width=14 if text == "Delete Selected" else 10, command=cmd).pack(side="left", padx=4)

        # Table Setup...
        right = tk.Frame(base_frame); right.pack(side="right", fill="both", expand=True, padx=8)
        self.tree = ttk.Treeview(right, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, anchor="w", width=140 if len(cols) == 5 else 160)
        self.tree.pack(fill="both", expand=True, side="left")
        scr = ttk.Scrollbar(right, orient="vertical", command=self.tree.yview); self.tree.configure(yscroll=scr.set); scr.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", double_click_handler)
        
        return self.tree

    # --- Patient Screen (P) ---
    def build_patients_tab(self):
        fields = [
            ("Patient ID (blank for new):", 'p_id', tk.Entry),
            ("Name:", 'p_name', tk.Entry),
            ("Birthdate (YYYY-MM-DD):", 'p_bdate', tk.Entry),
            ("Phone:", 'p_phone', tk.Entry),
            ("Gender:", 'p_gender', ttk.Combobox, ['Male', 'Female', 'Other'])
        ]
        callbacks = [
            ("Add", self._p_add), ("Update", self._p_update),
            ("Delete Selected", self._p_delete), ("Clear", self.clear_patient_fields),
            ("Refresh", self.load_patients)
        ]
        self.p_tree = self.setup_base_screen(self.tab_patients, fields, callbacks, ("id", "name", "birthdate", "phone", "gender"), self.on_patient_double, self.load_patients)
        self.p_fields = self.fields
        # Add live validation to the Patient Name entry to disallow digits
        try:
            vcmd_alpha = (self.root.register(self._validate_alpha), '%P')
            if 'p_name' in self.p_fields and isinstance(self.p_fields['p_name'], tk.Entry):
                self.p_fields['p_name'].config(validate='key', validatecommand=vcmd_alpha)
        except Exception:
            pass
        # Add live validation to the Patient Phone entry to restrict characters
        try:
            vcmd_phone = (self.root.register(self._validate_phone_chars), '%P')
            if 'p_phone' in self.p_fields and isinstance(self.p_fields['p_phone'], tk.Entry):
                self.p_fields['p_phone'].config(validate='key', validatecommand=vcmd_phone)
        except Exception:
            pass
        self.load_patients()

    def load_patients(self):
        for r in self.p_tree.get_children(): self.p_tree.delete(r)
        for row in s.load_entities("patients"):
            # rows are dicts from DictCursor: {'patient_id','name','birthdate','phone','gender'}
            bdate = row.get('birthdate').isoformat() if row.get('birthdate') else ""
            phone = row.get('phone') or ""
            gender = row.get('gender') or ""
            self.p_tree.insert("", "end", values=(row.get('patient_id'), row.get('name'), bdate, phone, gender))
        
    def clear_patient_fields(self):
        for k in self.p_fields: 
            if isinstance(self.p_fields[k], tk.Entry): self.p_fields[k].delete(0, tk.END)

    def _p_add(self):
        name = self.p_fields['p_name'].get().strip(); bdate = self.p_fields['p_bdate'].get().strip()
        # Validate name contains only alphabetic characters, spaces, hyphens, periods or apostrophes
        if not re.match(r"^[A-Za-z\s\-\.']+$", name):
            messagebox.showerror("Error", "Name must contain only alphabetic characters, spaces, hyphens, periods, or apostrophes.")
            return
        phone = self.p_fields['p_phone'].get().strip(); gender = self.p_fields['p_gender_var'].get()
        if not name: messagebox.showerror("Error", "Name required"); return
        try: s.add_patient(name, bdate, phone, gender); messagebox.showinfo("Success", "Patient added"); self.clear_patient_fields(); self.load_patients()
        except Exception as e: messagebox.showerror("Error", str(e))
    
    def _p_update(self):
        pid = self.p_fields['p_id'].get().strip()
        if not pid: messagebox.showerror("Error", "Enter patient ID (or double-click a row)."); return
        name = self.p_fields['p_name'].get().strip(); bdate = self.p_fields['p_bdate'].get().strip()
        if not re.match(r"^[A-Za-z\s\-\.']+$", name):
            messagebox.showerror("Error", "Name must contain only alphabetic characters, spaces, hyphens, periods, or apostrophes.")
            return
        phone = self.p_fields['p_phone'].get().strip(); gender = self.p_fields['p_gender_var'].get()
        if not name: messagebox.showerror("Error", "Name required"); return
        try: s.update_patient(pid, name, bdate, phone, gender); messagebox.showinfo("Success", f"Patient {pid} updated"); self.load_patients()
        except Exception as e: messagebox.showerror("Error", str(e))
        
    def _p_delete(self):
        sel = self.p_tree.selection()
        if not sel: messagebox.showerror("Error", "Select a patient row first."); return
        pid = self.p_tree.item(sel[0], "values")[0]
        # Confirmation message updated for ON DELETE CASCADE
        if messagebox.askyesno("Confirm", f"Delete patient {pid}? All associated sessions will also be deleted."):
            try: s.delete_entity("patients", pid); messagebox.showinfo("Deleted", f"Patient {pid} deleted"); self.load_patients()
            except Exception as e: messagebox.showerror("Error", str(e))

    def on_patient_double(self, event):
        sel = self.p_tree.selection(); 
        if not sel: return
        vals = self.p_tree.item(sel[0], "values")
        self.p_fields['p_id'].delete(0, tk.END); self.p_fields['p_id'].insert(0, vals[0])
        self.p_fields['p_name'].delete(0, tk.END); self.p_fields['p_name'].insert(0, vals[1])
        self.p_fields['p_bdate'].delete(0, tk.END); self.p_fields['p_bdate'].insert(0, vals[2])
        self.p_fields['p_phone'].delete(0, tk.END); self.p_fields['p_phone'].insert(0, vals[3] if vals[3] else "")
        self.p_fields['p_gender_var'].set(vals[4] if vals[4] else "")
    
    # --- Doctor Screen (D) ---
    def build_doctors_tab(self):
        # Use a Combobox for Specialty so users pick from standardized list
        specialty_options = [
            'General', 'Cardiology', 'Dermatology', 'Neurology', 'Pediatrics',
            'Oncology', 'Orthopedics', 'ENT', 'Emergency', 'Other'
        ]
        fields = [
            ("Doctor ID (blank for new):", 'd_id', tk.Entry),
            ("Name:", 'd_name', tk.Entry),
            ("Specialty:", 'd_spec', ttk.Combobox, specialty_options),
            ("Phone:", 'd_phone', tk.Entry),
            ("Gender:", 'd_gender', ttk.Combobox, ['Male', 'Female', 'Other'])
        ]
        callbacks = [
            ("Add", self._d_add), ("Update", self._d_update),
            ("Delete Selected", self._d_delete), ("Clear", self.clear_doctor_fields),
            ("Refresh", self.load_doctors)
        ]
        self.d_tree = self.setup_base_screen(self.tab_doctors, fields, callbacks, ("id", "name", "specialty", "phone", "gender"), self.on_doctor_double, self.load_doctors)
        self.d_fields = self.fields
        # Add live validation to the Name entry to disallow digits
        try:
            vcmd_alpha = (self.root.register(self._validate_alpha), '%P')
            if 'd_name' in self.d_fields and isinstance(self.d_fields['d_name'], tk.Entry):
                self.d_fields['d_name'].config(validate='key', validatecommand=vcmd_alpha)
        except Exception:
            pass
        # Add live validation to the Doctor Phone entry to restrict characters
        try:
            vcmd_phone = (self.root.register(self._validate_phone_chars), '%P')
            if 'd_phone' in self.d_fields and isinstance(self.d_fields['d_phone'], tk.Entry):
                self.d_fields['d_phone'].config(validate='key', validatecommand=vcmd_phone)
        except Exception:
            pass
        self.load_doctors()

    def load_doctors(self):
        for r in self.d_tree.get_children(): self.d_tree.delete(r)
        for row in s.load_entities("doctors"):
            # rows are dicts: {'doctor_id','name','specialty','phone','gender'}
            phone = row.get('phone') or ""
            gender = row.get('gender') or ""
            self.d_tree.insert("", "end", values=(row.get('doctor_id'), row.get('name'), row.get('specialty'), phone, gender))

    def clear_doctor_fields(self):
        for k in list(self.d_fields.keys()):
            v = self.d_fields[k]
            if isinstance(v, tk.Entry):
                v.delete(0, tk.END)
            elif isinstance(v, ttk.Combobox):
                # combobox has an associated variable stored under '{key}_var'
                var_key = f"{k}_var"
                if var_key in self.d_fields:
                    try:
                        self.d_fields[var_key].set("")
                    except Exception:
                        pass

    def _d_add(self):
        name = self.d_fields['d_name'].get().strip()
        # Validate name contains only alphabetic characters, spaces, hyphens, periods or apostrophes
        if not re.match(r"^[A-Za-z\s\-\.']+$", name):
            messagebox.showerror("Error", "Name must contain only alphabetic characters, spaces, hyphens, periods, or apostrophes.")
            return
        # read specialty from var if present (combobox), otherwise widget
        spec = self.d_fields['d_spec_var'].get().strip() if 'd_spec_var' in self.d_fields else self.d_fields['d_spec'].get().strip()
        phone = self.d_fields['d_phone'].get().strip(); gender = self.d_fields['d_gender_var'].get()
        if not name: messagebox.showerror("Error", "Name required"); return
        try: s.add_doctor(name, spec, phone, gender); messagebox.showinfo("Success", "Doctor added"); self.clear_doctor_fields(); self.load_doctors()
        except Exception as e: messagebox.showerror("Error", str(e))
    
    def _d_update(self):
        did = self.d_fields['d_id'].get().strip()
        if not did: messagebox.showerror("Error", "Enter doctor ID"); return
        name = self.d_fields['d_name'].get().strip()
        if not re.match(r"^[A-Za-z\s\-\.']+$", name):
            messagebox.showerror("Error", "Name must contain only alphabetic characters, spaces, hyphens, periods, or apostrophes.")
            return
        spec = self.d_fields['d_spec_var'].get().strip() if 'd_spec_var' in self.d_fields else self.d_fields['d_spec'].get().strip()
        phone = self.d_fields['d_phone'].get().strip(); gender = self.d_fields['d_gender_var'].get()
        if not name: messagebox.showerror("Error", "Name required"); return
        try: s.update_doctor(did, name, spec, phone, gender); messagebox.showinfo("Success", f"Doctor {did} updated"); self.load_doctors()
        except Exception as e: messagebox.showerror("Error", str(e))
        
    def _d_delete(self):
        sel = self.d_tree.selection()
        if not sel: messagebox.showerror("Error", "Select doctor row first"); return
        did = self.d_tree.item(sel[0], "values")[0]
        # Confirmation message updated for ON DELETE CASCADE
        if messagebox.askyesno("Confirm", f"Delete doctor {did}? All associated sessions will also be deleted."):
            try: s.delete_entity("doctors", did); messagebox.showinfo("Deleted", f"Doctor {did} deleted"); self.load_doctors()
            except Exception as e: messagebox.showerror("Error", str(e))

    def on_doctor_double(self, event):
        sel = self.d_tree.selection()
        if not sel: return
        vals = self.d_tree.item(sel[0], "values")
        self.d_fields['d_id'].delete(0, tk.END); self.d_fields['d_id'].insert(0, vals[0])
        self.d_fields['d_name'].delete(0, tk.END); self.d_fields['d_name'].insert(0, vals[1])
        # Specialty may be a combobox (has 'd_spec_var')
        if 'd_spec_var' in self.d_fields:
            self.d_fields['d_spec_var'].set(vals[2] if vals[2] else "")
        else:
            self.d_fields['d_spec'].delete(0, tk.END); self.d_fields['d_spec'].insert(0, vals[2])
        self.d_fields['d_phone'].delete(0, tk.END); self.d_fields['d_phone'].insert(0, vals[3] if vals[3] else "")
        self.d_fields['d_gender_var'].set(vals[4] if vals[4] else "")

    # --- Treatment Screen (T) ---
    def build_treatments_tab(self):
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
        self.t_tree = self.setup_base_screen(self.tab_treatments, fields, callbacks, ("id", "name", "cost"), self.on_treatment_double, self.load_treatments)
        self.t_fields = self.fields
        
        # Apply name validation
        try:
            vcmd_alpha = (self.root.register(self._validate_alpha), '%P')
            if 't_name' in self.t_fields and isinstance(self.t_fields['t_name'], tk.Entry):
                self.t_fields['t_name'].config(validate='key', validatecommand=vcmd_alpha)
        except Exception:
            pass
            
        # Apply cost validation
        try:
            vcmd_cost = (self.root.register(self._validate_cost_input), '%P')
            if 't_cost' in self.t_fields and isinstance(self.t_fields['t_cost'], tk.Entry):
                self.t_fields['t_cost'].config(validate='key', validatecommand=vcmd_cost)
        except Exception:
            pass

        self.load_treatments()

    def load_treatments(self):
        for r in self.t_tree.get_children(): self.t_tree.delete(r)
        for row in s.load_entities("treatments"):
            # rows are dicts: {'treatment_id','name','cost'}
            cost = float(row.get('cost')) if row.get('cost') is not None else 0.0
            self.t_tree.insert("", "end", values=(row.get('treatment_id'), row.get('name'), cost))

    def clear_treatment_fields(self):
        for k in self.t_fields: 
            if isinstance(self.t_fields[k], tk.Entry): self.t_fields[k].delete(0, tk.END)

    def _is_treatment_name_unique(self, name: str, exclude_id: str = None) -> bool:
        """Checks if a treatment name is unique across all treatments, excluding an ID if provided."""
        existing_treatments = s.load_entities("treatments")
        
        # Case insensitive comparison
        normalized_name = name.lower()
        
        for treatment in existing_treatments:
            tid = treatment.get('treatment_id')
            tname = treatment.get('name', '').lower()
            
            # Check if names match AND the current ID is NOT the one we are excluding
            if normalized_name == tname and (exclude_id is None or str(tid) != str(exclude_id)):
                return False
        return True

    def _t_add(self):
        name = self.t_fields['t_name'].get().strip(); cost_s = self.t_fields['t_cost'].get().strip()
        
        if not name: messagebox.showerror("Error", "Name required"); return
        
        # 1. Unique Name Check
        if not self._is_treatment_name_unique(name):
            messagebox.showerror("Error", f"Treatment name '{name}' already exists. Name must be unique.")
            return
            
        # 2. Non-Negative Cost Check
        try:
            cost = float(cost_s or 0.0)
            if cost < 0:
                messagebox.showerror("Error", "Cost cannot be negative.")
                return
        except ValueError:
            messagebox.showerror("Error", "Cost must be a valid number (e.g., 150.00).")
            return
            
        # 3. Add to Service
        try: 
            s.add_treatment(name, cost); messagebox.showinfo("Success", "Treatment added"); self.clear_treatment_fields(); self.load_treatments()
        except Exception as e: 
            messagebox.showerror("Error", str(e))
    
    def _t_update(self):
        tid = self.t_fields['t_id'].get().strip()
        if not tid: messagebox.showerror("Error", "Enter treatment ID"); return
        
        name = self.t_fields['t_name'].get().strip(); cost_s = self.t_fields['t_cost'].get().strip()
        if not name: messagebox.showerror("Error", "Name required"); return
        
        # 1. Unique Name Check (Excluding the current ID)
        if not self._is_treatment_name_unique(name, exclude_id=tid):
            messagebox.showerror("Error", f"Treatment name '{name}' already exists. Name must be unique.")
            return

        # 2. Non-Negative Cost Check
        try:
            cost = float(cost_s or 0.0)
            if cost < 0:
                messagebox.showerror("Error", "Cost cannot be negative.")
                return
        except ValueError:
            messagebox.showerror("Error", "Cost must be a valid number (e.g., 150.00).")
            return

        # 3. Update Service
        try: 
            s.update_treatment(tid, name, cost); messagebox.showinfo("Success", f"Treatment {tid} updated"); self.load_treatments()
        except Exception as e: 
            messagebox.showerror("Error", str(e))
        
    def _t_delete(self):
        sel = self.t_tree.selection()
        if not sel: messagebox.showerror("Error", "Select treatment row first"); return
        tid = self.t_tree.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirm", f"Delete treatment {tid}? Sessions will set treatment_id NULL."):
            try: s.delete_entity("treatments", tid); messagebox.showinfo("Deleted", f"Treatment {tid} deleted"); self.load_treatments()
            except Exception as e: messagebox.showerror("Error", str(e))

    def on_treatment_double(self, event):
        sel = self.t_tree.selection()
        if not sel: return
        vals = self.t_tree.item(sel[0], "values")
        self.t_fields['t_id'].delete(0, tk.END); self.t_fields['t_id'].insert(0, vals[0])
        self.t_fields['t_name'].delete(0, tk.END); self.t_fields['t_name'].insert(0, vals[1])
        self.t_fields['t_cost'].delete(0, tk.END); self.t_fields['t_cost'].insert(0, str(vals[2]))

    # --- Session Screen (S) ---
    def build_sessions_tab(self):
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
        self.s_tree = self.setup_base_screen(self.tab_sessions, fields, callbacks, ("id", "patient", "doctor", "treatment", "date"), self.on_session_double, self.load_sessions)
        self.s_fields = self.fields
        self.load_sessions()

    def load_sessions(self):
        p_vals, d_vals, t_vals = s.get_session_fk_data()
        self.s_fields['s_patient']["values"] = p_vals
        self.s_fields['s_doctor']["values"] = d_vals
        self.s_fields['s_treatment']["values"] = t_vals
        
        for r in self.s_tree.get_children(): self.s_tree.delete(r)
        for row in s.load_sessions_data():
            # row is a dict; keys depend on the SELECT aliasing
            sid = row.get('session_id')
            # Use explicit keys where available; fall back to generic names
            patient_display = f"{row.get('patient_id')}: {row.get('Patient_Name') or row.get('name') or ''}" if row.get('patient_id') else ""
            doctor_display = f"{row.get('doctor_id')}: {row.get('Doctor_Name') or row.get('name') or ''}" if row.get('doctor_id') else ""
            treat_display = f"{row.get('treatment_id')}: {row.get('Treatment_Name') or row.get('name') or ''}" if row.get('treatment_id') else ""
            tdate = None
            if row.get('treatment_date'):
                tdate = row.get('treatment_date')
            elif row.get('Date'):
                tdate = row.get('Date')
            tdate = tdate.isoformat() if tdate else ""
            self.s_tree.insert("", "end", values=(sid, patient_display, doctor_display, treat_display, tdate))

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
        sel = self.s_tree.selection()
        if not sel: messagebox.showerror("Error", "Select session row first"); return
        sid = self.s_tree.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirm", f"Delete session {sid}?"):
            try: s.delete_entity("sessions", sid); messagebox.showinfo("Deleted", f"Session {sid} deleted"); self.load_sessions()
            except Exception as e: messagebox.showerror("Error", str(e))

    def _get_id_from_display(self, display_string):
        """Extracts the ID from a display string like '123: Name'."""
        if display_string and ":" in display_string:
            try:
                # Use find(':') to handle potential ':' in the Name itself
                return display_string[:display_string.find(':')].strip()
            except:
                return None
        return None

    def on_session_double(self, event):
        sel = self.s_tree.selection(); 
        if not sel: return
        vals = self.s_tree.item(sel[0], "values")
        
        self.s_fields['s_id'].delete(0, tk.END); 
        self.s_fields['s_id'].insert(0, vals[0])

        # Helper to safely set combobox values based on the ID,
        # ensuring the value exactly matches one of the combobox options.
        def safe_set_fk(var_name, treeview_val, cb_widget):
            tree_id = self._get_id_from_display(treeview_val)
            found_match = ""
            if tree_id:
                # Iterate through options to find the exact match by ID
                for option in cb_widget['values']:
                    if option.startswith(f"{tree_id}:"):
                        found_match = option
                        break
            
            # Set the exact match, or the raw value (which will clear the combobox
            # if no exact match was found, e.g., if the FK is NULL).
            self.s_fields[var_name].set(found_match or treeview_val) 

        # Patient (vals[1])
        safe_set_fk('s_patient_var', vals[1], self.s_fields['s_patient'])
        
        # Doctor (vals[2]) - FIX IMPLEMENTATION
        safe_set_fk('s_doctor_var', vals[2], self.s_fields['s_doctor'])

        # Treatment (vals[3])
        safe_set_fk('s_treatment_var', vals[3], self.s_fields['s_treatment'])

        self.s_fields['s_date'].delete(0, tk.END); 
        self.s_fields['s_date'].insert(0, vals[4])

    # =========================================================================
    # NEW: GLOBAL SEARCH TAB
    # =========================================================================

    def build_global_search_tab(self):
        frame = self.tab_global_search
        
        # --- Top Search Frame ---
        top = ttk.Frame(frame, padding=10)
        top.pack(fill="x")
        
        ttk.Label(top, text="Global Search (Patient/Doctor/Treatment Name):").pack(side="left", padx=5)
        
        self.g_search = tk.StringVar()
        ttk.Entry(top, textvariable=self.g_search, width=40).pack(side="left", padx=5)
        
        ttk.Button(top, text="Search Sessions", command=self.global_search_sessions).pack(side="left", padx=5)
        
        # --- Results Treeview ---
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        vscroll = ttk.Scrollbar(tree_frame, orient="vertical")
        hscroll = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.g_search_tree = ttk.Treeview(tree_frame, 
                                          columns=(), 
                                          show="headings", 
                                          yscrollcommand=vscroll.set, 
                                          xscrollcommand=hscroll.set)
        
        vscroll.config(command=self.g_search_tree.yview)
        hscroll.config(command=self.g_search_tree.xview)
        
        vscroll.pack(side="right", fill="y")
        hscroll.pack(side="bottom", fill="x")
        self.g_search_tree.pack(fill="both", expand=True)
        

    def global_search_sessions(self):
        kw = self.g_search.get().strip()
        if not kw:
            messagebox.showinfo("Info", "Enter search keyword")
            return
            
        self.g_search_tree.delete(*self.g_search_tree.get_children())
        
        sql = q.G_SEARCH
        p = f"%{kw}%"
        
        try:
            con = s.get_connection()
            if not con: return
            cur = con.cursor()
            
            cur.execute(sql, (p, p, p))
            rows = cur.fetchall()
            con.close()
            
            if not rows:
                self._set_global_search_columns([])
                return
            
            cols = list(rows[0].keys())
            self._set_global_search_columns(cols)
            
            for r in rows:
                vals = [r[c] for c in cols]
                vals = [fmt_date(v) if isinstance(v, (datetime, date)) else v for v in vals] 
                self.g_search_tree.insert("", "end", values=vals)
                
        except Exception as e:
            messagebox.showerror("Search Error", f"Error during global search: {e}")
            
            
    def _set_global_search_columns(self, cols):
        self.g_search_tree["columns"] = cols
        for c in cols:
            self.g_search_tree.heading(c, text=c)
            self.g_search_tree.column(c, width=150, anchor="w")
        self.g_search_tree.delete(*self.g_search_tree.get_children())
        
    # =========================================================================
    # NEW: REPORTS TAB
    # =========================================================================

    def build_reports_tab(self):
        frame = self.tab_reports
        
        # --- Reports/Queries List (Left side) ---
        query_list_frame = ttk.LabelFrame(frame, text="Reports/Queries", padding=10)
        query_list_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        ttk.Label(query_list_frame, text="1. Inner Join:").pack(anchor="w", pady=(5, 0))
        ttk.Button(query_list_frame, text="Sessions by Patient/Treatment", command=self.report_inner_join).pack(fill="x", pady=2)

        ttk.Label(query_list_frame, text="2. Left Join:").pack(anchor="w", pady=(10, 0))
        ttk.Button(query_list_frame, text="All Patients (with/without Sessions)", command=self.report_left_join).pack(fill="x", pady=2)
        
        ttk.Label(query_list_frame, text="3. Multi-Table Join:").pack(anchor="w", pady=(10, 0))
        ttk.Button(query_list_frame, text="Sessions (P, D, T)", command=self.report_multi_join).pack(fill="x", pady=2)

        ttk.Label(query_list_frame, text="4. Subquery/Aggregation:").pack(anchor="w", pady=(10, 0))
        ttk.Button(query_list_frame, text="High-cost Treatments & Patients", command=self.report_high_cost).pack(fill="x", pady=2)

        ttk.Separator(query_list_frame, orient="horizontal").pack(fill="x", pady=10)
        ttk.Button(query_list_frame, text="Export Report CSV", command=self.export_report_csv).pack(fill="x", pady=5)
        
        # --- Report Output (Right side) ---
        report_frame = ttk.LabelFrame(frame, text="Report Results", padding=10)
        report_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        vscroll = ttk.Scrollbar(report_frame, orient="vertical")
        hscroll = ttk.Scrollbar(report_frame, orient="horizontal")
        self.report_tree = ttk.Treeview(report_frame, show="headings", yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)
        
        vscroll.config(command=self.report_tree.yview)
        hscroll.config(command=self.report_tree.xview)
        
        vscroll.pack(side="right", fill="y")
        hscroll.pack(side="bottom", fill="x")
        self.report_tree.pack(fill="both", expand=True)

        self.report_inner_join() 

    def set_report_columns(self, cols):
        self.report_tree.delete(*self.report_tree.get_children())
        self.report_tree["columns"] = cols
        for c in cols:
            self.report_tree.heading(c, text=c)
            self.report_tree.column(c, width=150)

    def report_inner_join(self):
        sql = """
            SELECT p.name AS Patient, t.name AS Treatment, s.treatment_date AS Date, t.cost AS Cost
            FROM sessions s
            JOIN patients p ON s.patient_id = p.patient_id
            JOIN treatments t ON s.treatment_id = t.treatment_id
            ORDER BY s.treatment_date DESC
        """
        self.run_report_sql(sql)

    def report_left_join(self):
        sql = """
            SELECT p.name AS Patient, t.name AS Treatment, s.treatment_date AS Date, t.cost AS Cost
            FROM patients p
            LEFT JOIN sessions s ON p.patient_id = s.patient_id
            LEFT JOIN treatments t ON s.treatment_id = t.treatment_id
            ORDER BY p.patient_id
        """
        self.run_report_sql(sql)

    def report_multi_join(self):
        sql = """
            SELECT p.name AS Patient, d.name AS Doctor, t.name AS Treatment, s.treatment_date AS Date, t.cost AS Cost
            FROM sessions s
            JOIN patients p ON s.patient_id = p.patient_id
            JOIN doctors d ON s.doctor_id = d.doctor_id
            JOIN treatments t ON s.treatment_id = t.treatment_id
            ORDER BY s.treatment_date DESC
        """
        self.run_report_sql(sql)

    def report_high_cost(self):
        sql = """
            SELECT t.name AS Treatment, t.cost AS Cost, p.name AS Patient
            FROM treatments t
            LEFT JOIN sessions s ON t.treatment_id = s.treatment_id
            LEFT JOIN patients p ON s.patient_id = p.patient_id
            WHERE t.cost > (SELECT AVG(cost) FROM treatments)
            ORDER BY t.cost DESC
        """
        self.run_report_sql(sql)

    def run_report_sql(self, sql, params=None):
        con = s.get_connection()
        if not con: return
        try:
            cur = con.cursor()
            cur.execute(sql, params or ())
            rows = cur.fetchall()
            
            if not rows:
                self.set_report_columns([])
                return
                
            cols = list(rows[0].keys())
            self.set_report_columns(cols)
            for r in rows:
                vals = [r[c] for c in cols]
                vals = [fmt_date(v) if isinstance(v, (datetime, date)) 
                        else (float(v) if isinstance(v, (decimal.Decimal,)) else v) 
                        for v in vals]
                self.report_tree.insert("", "end", values=vals)
        except Exception as e:
            messagebox.showerror("Report Error", f"SQL execution failed: {e}")
        finally:
            if con: con.close()

    def export_report_csv(self):
        rows = [self.report_tree.item(i)["values"] for i in self.report_tree.get_children()]
        if not rows:
            messagebox.showinfo("Export", "No data to export")
            return
            
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path: return
            
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                cols = self.report_tree["columns"]
                w.writerow(cols)
                for r in rows:
                    w.writerow(r)
            messagebox.showinfo("Exported", f"Saved to {path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export CSV: {e}")