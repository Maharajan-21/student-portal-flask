import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

cursor.execute("""
ALTER TABLE students
ADD COLUMN cgpa REAL
""")

connection.commit()
connection.close()

print("CGPA column added successfully!")