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
        cost DECIMAL(10,2)
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
P_SELECT_ALL = "SELECT patient_id, name, birthdate FROM patients ORDER BY patient_id"
P_INSERT = "INSERT INTO patients (name, birthdate) VALUES (%s,%s)"
P_UPDATE = "UPDATE patients SET name=%s, birthdate=%s WHERE patient_id=%s"
P_DELETE = "DELETE FROM patients WHERE patient_id=%s"
P_SEARCH = "SELECT id, name, birthdate FROM patients WHERE id LIKE %s OR name LIKE %s"

# Doctor Queries
D_SELECT_ALL = "SELECT doctor_id, name, specialty FROM doctors ORDER BY doctor_id"
D_INSERT = "INSERT INTO doctors (name, specialty) VALUES (%s,%s)"
D_UPDATE = "UPDATE doctors SET name=%s, specialty=%s WHERE doctor_id=%s"
D_DELETE = "DELETE FROM doctors WHERE doctor_id=%s"
D_SEARCH = "SELECT id, name, specialty FROM doctors WHERE id LIKE %s OR name LIKE %s"

# Treatment Queries
T_SELECT_ALL = "SELECT treatment_id, name, cost FROM treatments ORDER BY treatment_id"
T_INSERT = "INSERT INTO treatments (name, cost) VALUES (%s,%s)"
T_UPDATE = "UPDATE treatments SET name=%s, cost=%s WHERE treatment_id=%s"
T_DELETE = "DELETE FROM treatments WHERE treatment_id=%s"
T_SEARCH = "SELECT id, name, cost FROM treatments WHERE id LIKE %s OR name LIKE %s"

# Session Queries
S_SELECT_ALL = """
    SELECT s.session_id, p.patient_id, p.name, d.doctor_id, d.name, t.treatment_id, t.name, s.treatment_date
    FROM sessions s
    LEFT JOIN patients p ON s.patient_id = p.patient_id
    LEFT JOIN doctors d ON s.doctor_id = d.doctor_id
    LEFT JOIN treatments t ON s.treatment_id = t.treatment_id
    ORDER BY s.session_id
"""
S_INSERT = "INSERT INTO sessions (patient_id, doctor_id, treatment_id, treatment_date) VALUES (%s,%s,%s,%s)"
S_UPDATE = "UPDATE sessions SET patient_id=%s, doctor_id=%s, treatment_id=%s, treatment_date=%s WHERE session_id=%s"
S_DELETE = "DELETE FROM sessions WHERE session_id=%s"
S_SEARCH = """
    SELECT s.id, s.name, p.name, d.name, s.treatment_date
    FROM sessions s
    JOIN patients p ON p.id = s.patient_id
    JOIN doctors d ON d.id = s.doctor_id
    WHERE s.id LIKE %s OR s.name LIKE %s OR p.name LIKE %s OR d.name LIKE %s
"""