import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

cursor.execute("""
ALTER TABLE students
ADD COLUMN attendance INTEGER
""")

connection.commit()
connection.close()

print("Attendance column added successfully!")