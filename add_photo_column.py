import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

cursor.execute("""
ALTER TABLE students
ADD COLUMN photo TEXT
""")

connection.commit()
connection.close()

print("Photo column added successfully!")