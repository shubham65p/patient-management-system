# appointment_repo.py
import logging
from database.db_protocol import Database

logger=logging.getLogger(__name__)
class AppointmentRepository:
    def __init__(self, db: Database):
        self.db = db

    def add(self, patient_id, appointment_no, consultation_fee):
        # cursor = self.conn.cursor()
        self.db.execute("""
            INSERT INTO appointments
            (patient_id, appointment_no, consultation_fee)
            VALUES (?, ?, ?)
        """, (patient_id, appointment_no, consultation_fee))
        self.db.commit()
        return self.db.lastrowid
    
    
    def get_appointment_by_patient_id(self, id):
        # cursor = self.conn.cursor()
        self.db.execute("""
            Select * from appointments
            Where patient_id = ?
        """, (id,))
        return self.db.fetchall()
    
    def delete_by_patient_id(self, id):
        # cursor = self.conn.cursor()
        try:
            self.db.execute("""
            DELETE appointments
            where patient_id = ?
            """,(id,))
        except Exception as e:
            logger.error(f"Error deleting appointments : {e}")
        
