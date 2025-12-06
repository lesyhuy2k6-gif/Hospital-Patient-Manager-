# services.py
from datetime import datetime
from tkinter import messagebox
from connection import get_connection
import queries as q

def ensure_tables():
    """Creates tables if they don't exist."""
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                for query in q.CREATE_TABLES: cur.execute(query)
                conn.commit()
        except Exception as e:
            messagebox.showerror("DB Setup Error", f"Could not ensure tables: {e}")
        finally:
            conn.close()

def db_execute(query, params=None, fetch=False, commit=False):
    """Generic utility to execute database operations."""
    conn = get_connection()
    if not conn: return []
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if commit: conn.commit()
            return cur.fetchall() if fetch else None
    except Exception as e:
        messagebox.showerror("DB Error", str(e))
        return []
    finally:
        conn.close()

def parse_date(s):
    """Expect YYYY-MM-DD. Return date string or raise ValueError."""
    if not s: return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date().isoformat()
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format")

# --- CRUD Operations ---
def load_entities(table_name):
    query = getattr(q, f"{table_name[0].upper()}_SELECT_ALL")
    rows = db_execute(query, fetch=True)
    return rows if rows else []

def add_patient(name, bdate_s):
    bdate = parse_date(bdate_s)
    db_execute(q.P_INSERT, (name, bdate), commit=True)

def update_patient(pid, name, bdate_s):
    bdate = parse_date(bdate_s)
    db_execute(q.P_UPDATE, (name, bdate, int(pid)), commit=True)

def delete_entity(table_name, entity_id):
    query = getattr(q, f"{table_name[0].upper()}_DELETE")
    db_execute(query, (int(entity_id),), commit=True)

def add_doctor(name, spec):
    db_execute(q.D_INSERT, (name, spec), commit=True)

def update_doctor(did, name, spec):
    db_execute(q.D_UPDATE, (name, spec, int(did)), commit=True)

def add_treatment(name, cost_s):
    cost = float(cost_s) if cost_s else 0.0
    db_execute(q.T_INSERT, (name, cost), commit=True)

def update_treatment(tid, name, cost_s):
    cost = float(cost_s) if cost_s else 0.0
    db_execute(q.T_UPDATE, (name, cost, int(tid)), commit=True)

def load_sessions_data():
    return db_execute(q.S_SELECT_ALL, fetch=True)

def get_session_fk_data():
    p = [f"{r[0]}: {r[1]}" for r in db_execute(q.P_SELECT_ALL.replace('birthdate', ''), fetch=True)]
    d = [f"{r[0]}: {r[1]}" for r in db_execute(q.D_SELECT_ALL.replace(', specialty', ''), fetch=True)]
    t = [f"{r[0]}: {r[1]}" for r in db_execute(q.T_SELECT_ALL.replace(', cost', ''), fetch=True)]
    return p, d, t

def add_session(p_var, d_var, t_var, date_s):
    date_val = parse_date(date_s)
    pid = int(p_var.split(":")[0]); did = int(d_var.split(":")[0]); tid = int(t_var.split(":")[0])
    db_execute(q.S_INSERT, (pid, did, tid, date_val), commit=True)

def update_session(sid, p_var, d_var, t_var, date_s):
    date_val = parse_date(date_s)
    pid = int(p_var.split(":")[0]); did = int(d_var.split(":")[0]); tid = int(t_var.split(":")[0])
    db_execute(q.S_UPDATE, (pid, did, tid, date_val, int(sid)), commit=True)

def search_entities(table, search_value):
    conn = get_connection()
    if not conn: return []
    try:
        with conn.cursor() as cursor:
            like_val = f"%{search_value}%"
            if table == "sessions":
                cursor.execute(q.S_SEARCH, (like_val, like_val, like_val, like_val))
            else:
                query = getattr(q, f"{table[0].upper()}_SEARCH")
                cursor.execute(query, (like_val, like_val))
            return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("DB Error", f"Error searching: {e}")
        return []
    finally:
        conn.close()