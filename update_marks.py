import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

students = [
    (485, 101),
    (450, 104),
    (475, 105),
    (490, 106),
    (430, 107),
    (410, 108),
    (395, 109),
    (500, 110)
]

for marks, student_id in students:

    cursor.execute("""
    UPDATE students
    SET marks=?
    WHERE student_id=?
    """, (marks, student_id))

connection.commit()
connection.close()

print("All Marks Updated!")