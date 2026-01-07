import sqlite3
from create_directory_for_database import create_dir
# from load_config import config
class DatabaseManager:
    def __init__(self):
        folder_name = create_dir()
        self.conn = sqlite3.connect(f'C:\\ProgramData\\{folder_name}\\patients.db')
        # self.conn = sqlite3.connect(f'C:\\ProgramData\\Patient Management System Database\\patients.db')

        # Prevents orphan records
        # Enforces relational integrity
        self.conn.execute("PRAGMA foreign_keys = ON")

        # Safer on crashes
        # Better concurrency
        # Less chance of DB corruption
        self.conn.execute("PRAGMA journal_mode = WAL")

        self.conn.execute("PRAGMA synchronous = FULL")
        self.create_table()
        self.ALLOWED_COLUMNS_FOR_SEARCH = {"name", "age", "email", "gender"}

    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
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
        ''')
        self.conn.commit()
    
    def add_patient(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO patients (name, age, gender, dob, phone, address, 
                                first_appointment, major_complain, followup_date, total_followups)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        self.conn.commit()
        return cursor.lastrowid
    
    def delete_patient(self, patient_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        self.conn.commit()
    
    def update_patient(self, patient_id, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE patients SET name=?, age=?, gender=?, dob=?, phone=?, 
                              address=?, first_appointment=?, major_complain=?, 
                              followup_date=?, total_followups=?
            WHERE id=?
        ''', (*data, patient_id))
        self.conn.commit()
    
    def search_patients(self, criteria, value):
        cursor = self.conn.cursor()
        
        if criteria not in self.ALLOWED_COLUMNS_FOR_SEARCH and criteria != "all":
            raise ValueError("Invalid column")
        if criteria == "all":
            cursor.execute('SELECT * FROM patients')
        elif criteria == 'gender':
            print('criteria: ', criteria)
            print('value: ', value)
            query = f'SELECT * FROM patients WHERE LOWER({criteria}) = LOWER(?)'
            cursor.execute(query, (f'{value}',))
        else:
            print('criteria: ', criteria)
            print('value: ', value)
            query = f'SELECT * FROM patients WHERE {criteria} LIKE ?'
            cursor.execute(query, (f'%{value}%',))
        return cursor.fetchall()
    
    def get_all_patients(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM patients ORDER BY id DESC')
        return cursor.fetchall()

