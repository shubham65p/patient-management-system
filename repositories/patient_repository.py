# # patient_repo.py
# class PatientRepository:
#     def __init__(self, conn):
#         self.conn = conn

#     def add(self, data):
#         cursor = self.conn.cursor()
#         my_data = (
#             data['name'],
#             data['age'],
#             data['gender'],
#             data['dob'],
#             data['phone'],
#             data['address'],
#             data['first_appointment'],
#             data['major_complain'],
#             data['followup_date'],
#             data['total_followups'],
            
#         )
        
#         cursor.execute("""
#             INSERT INTO patients
#             (name, age, gender, dob, phone, address,
#              first_appointment, major_complain, followup_date, total_followups)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, my_data)
#         self.conn.commit()
#         return cursor.lastrowid
    
#     def update(self, patient_id, data):
#         cursor = self.conn.cursor()
#         my_data = (
#             data['name'],
#             data['age'],
#             data['gender'],
#             data['dob'],
#             data['phone'],
#             data['address'],
#             data['first_appointment'],
#             data['major_complain'],
#             data['followup_date'],
#             data['total_followups'],
            
#         )
#         cursor.execute('''
#             UPDATE patients SET name=?, age=?, gender=?, dob=?, phone=?, 
#                               address=?, first_appointment=?, major_complain=?, 
#                               followup_date=?, total_followups=?
#             WHERE id=?
#         ''', (*my_data, patient_id))
#         self.conn.commit()

#     def get_all(self):
#         cursor = self.conn.cursor()
#         cursor.execute("SELECT * FROM patients ORDER BY id DESC")
#         return cursor.fetchall()

from data_validation import Patient
from database.db_protocol import Database
# -------------------------------------------------------------------------
# Repository should not know that SQLite exist, it should know that some database exist (what database it is and how it works should not matter to repository thats how we create abstraction of database to repository)
# Repository depends on expectation, not the implementation
# -------------------------------------------------------------------------
# High-level modules should not depend on low-level modules.
# Both should depend on abstractions.

# Abstractions should not depend on details.
# Details should depend on abstractions.
# -------------------------------------------------------------------------
# High-level module
#     Contains business logic
#     Makes decisions
#     Example:
#         PatientRepository
#         PatientService
#         “Save patient”, “Search patient”

# Low-level module
#     Contains implementation details
#     Talks to external systems
#     Example:
#         SQLite
#         PostgreSQL
#         File system
#         HTTP
#         Redis
# -------------------------------------------------------------------------
# “Repository depends on what it needs, not who provides it”
# -------------------------------------------------------------------------


class PatientRepository:
    # ALLOWED_COLUMNS_FOR_SEARCH = {"name", "age", "email", "gender"}
    def __init__(self, db: Database):
        self.db = db
        

    def add(self, patient: Patient) -> int:
        # cursor = self.conn.cursor()

        # data = patient.model_dump()
        data = patient.model_dump(exclude_none=False)

        my_data = (
            data["name"],
            data["age"],
            data["gender"],
            data["dob"],
            data["phone"],
            data["address"],
            data["first_appointment"],
            data["major_complain"],
            data["followup_date"],
            data["total_followups"],
        )

        self.db.execute(
            """
            INSERT INTO patients
            (name, age, gender, dob, phone, address,
             first_appointment, major_complain, followup_date, total_followups)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            my_data
        )

        self.db.commit()
        return self.db.lastrowid

    def update(self, patient_id: int, patient: Patient) -> None:
        # cursor = self.conn.cursor()
        data = patient.model_dump(exclude_none=False)

        my_data = (
            data["name"],
            data["age"],
            data["gender"],
            data["dob"],
            data["phone"],
            data["address"],
            data["first_appointment"],
            data["major_complain"],
            data["followup_date"],
            data["total_followups"],
        )

        self.db.execute(
            """
            UPDATE patients
            SET name=?, age=?, gender=?, dob=?, phone=?,
                address=?, first_appointment=?, major_complain=?,
                followup_date=?, total_followups=?
            WHERE id=?
            """,
            (*my_data, patient_id)
        )

        self.db.commit()

    def get_all(self):
        # cursor = self.conn.cursor()
        self.db.execute("SELECT * FROM patients ORDER BY id DESC")
        return self.db.fetchall()
    
    def delete_patient(self, patient_id):
        # cursor = self.db.cursor()
        self.db.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        self.db.commit()

    def execute_query(self, query: str, params: tuple = ()):
        self.db.execute(query, params)
        return self.db.fetchall()

    # def search_patients(self, criteria, value):
    #     # cursor = self.conn.cursor()
        
    #     if criteria not in self.ALLOWED_COLUMNS_FOR_SEARCH and criteria != "all":
    #         raise ValueError("Invalid column")
    #     if criteria == "all":
    #         self.db.execute('SELECT * FROM patients')
    #     elif criteria == 'gender':
    #         print('criteria: ', criteria)
    #         print('value: ', value)
    #         query = f'SELECT * FROM patients WHERE LOWER({criteria}) = LOWER(?)'
    #         self.db.execute(query, (f'{value}',))
    #     else:
    #         print('criteria: ', criteria)
    #         print('value: ', value)
    #         query = f'SELECT * FROM patients WHERE {criteria} LIKE ?'
    #         self.db.execute(query, (f'%{value}%',))
    #     return self.db.fetchall()

    
