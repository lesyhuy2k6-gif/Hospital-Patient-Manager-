# queries.py
CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        specialty VARCHAR(100)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        birthdate DATE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS treatments (
        treatment_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        cost DECIMAL(10,2) -- Note: Column name is 'cost'
    )
    """,
    """
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
    """
]

# Patient Queries
P_SELECT_ALL = "SELECT patient_id, name, birthdate, phone, gender FROM patients ORDER BY patient_id"
P_INSERT = "INSERT INTO patients (name, birthdate, phone, gender) VALUES (%s,%s,%s,%s)"
P_UPDATE = "UPDATE patients SET name=%s, birthdate=%s, phone=%s, gender=%s WHERE patient_id=%s"
P_DELETE = "DELETE FROM patients WHERE patient_id=%s"
P_SEARCH = "SELECT patient_id, name, birthdate, phone, gender FROM patients WHERE patient_id LIKE %s OR name LIKE %s"

# Doctor Queries - FIX: Replaced 'id' with 'doctor_id'
D_SELECT_ALL = "SELECT doctor_id, name, specialty, phone, gender FROM doctors ORDER BY doctor_id"
D_INSERT = "INSERT INTO doctors (name, specialty, phone, gender) VALUES (%s,%s,%s,%s)"
D_UPDATE = "UPDATE doctors SET name=%s, specialty=%s, phone=%s, gender=%s WHERE doctor_id=%s"
D_DELETE = "DELETE FROM doctors WHERE doctor_id=%s"
D_SEARCH = "SELECT doctor_id, name, specialty, phone, gender FROM doctors WHERE doctor_id LIKE %s OR name LIKE %s"

# Treatment Queries - FIX: Replaced 'id' with 'treatment_id'
T_SELECT_ALL = "SELECT treatment_id, name, cost FROM treatments ORDER BY treatment_id"
T_INSERT = "INSERT INTO treatments (name, cost) VALUES (%s,%s)"
T_UPDATE = "UPDATE treatments SET name=%s, cost=%s WHERE treatment_id=%s"
T_DELETE = "DELETE FROM treatments WHERE treatment_id=%s"
T_SEARCH = "SELECT treatment_id, name, cost FROM treatments WHERE treatment_id LIKE %s OR name LIKE %s"

# Session Queries
S_SELECT_ALL = """
    SELECT s.session_id,
           p.patient_id,
           p.name AS Patient_Name,
           d.doctor_id,
           d.name AS Doctor_Name,
           t.treatment_id,
           t.name AS Treatment_Name,
           s.treatment_date AS Date
    FROM sessions s
    LEFT JOIN patients p ON s.patient_id = p.patient_id
    LEFT JOIN doctors d ON s.doctor_id = d.doctor_id
    LEFT JOIN treatments t ON s.treatment_id = t.treatment_id
    ORDER BY s.session_id
"""
S_INSERT = "INSERT INTO sessions (patient_id, doctor_id, treatment_id, treatment_date) VALUES (%s,%s,%s,%s)"
S_UPDATE = "UPDATE sessions SET patient_id=%s, doctor_id=%s, treatment_id=%s, treatment_date=%s WHERE session_id=%s"
S_DELETE = "DELETE FROM sessions WHERE session_id=%s"

# --- NEW QUERIES FOR DASHBOARD & GLOBAL SEARCH ---

# Global Search Query (G_SEARCH)
G_SEARCH = """
    SELECT 
        s.session_id, 
        p.name AS Patient_Name, 
        d.name AS Doctor_Name, 
        t.name AS Treatment_Name, 
        t.cost AS Cost,
        s.treatment_date AS Date
    FROM sessions s
    LEFT JOIN patients p ON s.patient_id = p.patient_id
    LEFT JOIN doctors d ON s.doctor_id = d.doctor_id
    LEFT JOIN treatments t ON s.treatment_id = t.treatment_id
    WHERE 
        p.name LIKE %s OR d.name LIKE %s OR t.name LIKE %s
    ORDER BY s.treatment_date DESC
"""

# Dashboard Query (Q_TREATMENT_COST_DISTRIBUTION)
Q_TREATMENT_COST_DISTRIBUTION = "SELECT cost FROM treatments WHERE cost IS NOT NULL"