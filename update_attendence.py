import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

students = [
    (92, 101),
    (85, 104),
    (90, 105),
    (95, 106),
    (88, 107),
    (91, 108),
    (87, 109),
    (96, 110)
]

for attendance, student_id in students:

    cursor.execute("""
    UPDATE students
    SET attendance = ?
    WHERE student_id = ?
    """, (attendance, student_id))

connection.commit()
connection.close()

print("Attendance Updated Successfully!")