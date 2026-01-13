PATIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    dob TEXT,
    phone TEXT,
    address TEXT,
    first_appointment TEXT,
    major_complain TEXT,
    followup_date TEXT,
    total_followups INTEGER DEFAULT 0
)
"""

APPOINTMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    appointment_no INTEGER,
    consultation_fee INTEGER,
    FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
)
"""

MEDICINES_TABLE = """
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    name TEXT,
    fee INTEGER,
    FOREIGN KEY(appointment_id) REFERENCES appointments(id) ON DELETE CASCADE
)
"""

THERAPIES_TABLE = """
CREATE TABLE IF NOT EXISTS therapies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    name TEXT,
    fee INTEGER,
    FOREIGN KEY(appointment_id) REFERENCES appointments(id) ON DELETE CASCADE
)
"""
