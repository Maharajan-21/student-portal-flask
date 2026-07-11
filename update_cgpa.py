import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

students = [
    (9.2, 101),
    (8.8, 104),
    (8.5, 105),
    (9.5, 106),
    (8.9, 107),
    (8.7, 108),
    (8.2, 109),
    (9.8, 110)
]

for cgpa, student_id in students:

    cursor.execute("""
    UPDATE students
    SET cgpa = ?
    WHERE student_id = ?
    """, (cgpa, student_id))

connection.commit()
connection.close()

print("CGPA Updated Successfully!")