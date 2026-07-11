import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

cursor.execute("""
UPDATE students
SET photo = 'maha.jpg'
WHERE student_id = 101
""")

connection.commit()
connection.close()

print("Photo updated successfully!")