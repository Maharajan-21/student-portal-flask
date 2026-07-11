import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

cursor.execute("""
ALTER TABLE students
ADD COLUMN marks INTEGER
""")

connection.commit()
connection.close()

print("Marks column added successfully!")