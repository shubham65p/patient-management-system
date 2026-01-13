from database.SQLiteDB.connection import DatabaseConnection

conn = DatabaseConnection(f'C:\\ProgramData\\Patient Management System database\\patients.db').get_connection()

cursor = conn.cursor()

table = cursor.execute("Select * from appointments").fetchall()
print(table)

