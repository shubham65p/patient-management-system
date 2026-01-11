# patient_repo.py
class PatientRepository:
    def __init__(self, conn):
        self.conn = conn
        self.ALLOWED_COLUMNS_FOR_SEARCH = {"name", "age", "email", "gender"}

    def add(self, data):
        cursor = self.conn.cursor()
        my_data = (
            data['name'],
            data['age'],
            data['gender'],
            data['dob'],
            data['phone'],
            data['address'],
            data['first_appointment'],
            data['major_complain'],
            data['followup_date'],
            data['total_followups'],
            
        )
        
        cursor.execute("""
            INSERT INTO patients
            (name, age, gender, dob, phone, address,
             first_appointment, major_complain, followup_date, total_followups)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, my_data)
        self.conn.commit()
        return cursor.lastrowid
    
    def update(self, patient_id, data):
        cursor = self.conn.cursor()
        my_data = (
            data['name'],
            data['age'],
            data['gender'],
            data['dob'],
            data['phone'],
            data['address'],
            data['first_appointment'],
            data['major_complain'],
            data['followup_date'],
            data['total_followups'],
            
        )
        cursor.execute('''
            UPDATE patients SET name=?, age=?, gender=?, dob=?, phone=?, 
                              address=?, first_appointment=?, major_complain=?, 
                              followup_date=?, total_followups=?
            WHERE id=?
        ''', (*my_data, patient_id))
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM patients ORDER BY id DESC")
        return cursor.fetchall()
    
    def delete_patient(self, patient_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
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

    
