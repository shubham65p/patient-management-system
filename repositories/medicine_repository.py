# appointment_repo.py
from database.db_protocol import Database
class MedicineRepository:
    def __init__(self, db: Database):
        self.db = db

    def add(self, appointment_id: int, name: str, fee: int):
        # cursor = self.conn.cursor()
        self.db.execute("""
            INSERT INTO medicines (appointment_id, name, fee)
            VALUES (?, ?, ?)
        """, (appointment_id, name, fee))
        self.db.commit()
        return self.db.lastrowid
    
    def get_medicine_by_appointment_id(self, id):
        # cursor = self.conn.cursor()
        self.db.execute("""
            Select * from medicines
            Where appointment_id = ?
        """, (id,))
        return self.db.fetchall()

