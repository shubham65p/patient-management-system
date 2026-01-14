from database.SQLiteDB.connection import SQLiteConnection
from database.SQLiteDB.sqlite_database import SQLiteDatabase
from database.SQLiteDB.schema import SchemaManager
from create_directory_for_database import create_dir
from config import config

def create_database():
    folder = create_dir()
    conn = SQLiteConnection(
        f"C:\\ProgramData\\{folder}\\{config['database_name']}.db"
    ).get_connection()

    db = SQLiteDatabase(conn)
    SchemaManager(db).create_tables()
    return db
