from database.db_protocol import Database
from database.SQLiteDB.sql import (
    PATIENTS_TABLE,
    APPOINTMENTS_TABLE,
    MEDICINES_TABLE,
    THERAPIES_TABLE,
    USERS_TABLE
)

class SchemaManager:
    def __init__(self, db: Database):
        self.db = db

    def create_tables(self) -> None:
        for statement in (
            USERS_TABLE,
            PATIENTS_TABLE,
            APPOINTMENTS_TABLE,
            MEDICINES_TABLE,
            THERAPIES_TABLE,
        ):
            self.db.execute(statement)

        self.db.commit()
