from flask import Flask, render_template, request, redirect, url_for, session
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
import sqlite3

app = Flask(__name__)
app.secret_key = "mysecretkey"

@app.route("/") 
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM students
        WHERE name=? AND password=?
        """, (username, password))

        student = cursor.fetchone()

        connection.close()

        if student:
            session["student_id"] = student[0]
            return render_template("dashboard.html", student=student)

        else:
            return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        department = request.form["department"]
        password = request.form["password"]

        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO students(name, department, password)
        VALUES (?, ?, ?)
        """, (name, department, password))

        connection.commit()
        connection.close()

        return "Registration Successful ✅"

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():

    if "student_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM students
    WHERE student_id=?
    """, (session["student_id"],))

    student = cursor.fetchone()

    connection.close()

    return render_template("dashboard.html", student=student)


@app.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    if request.method == "POST":

        name = request.form["name"]
        department = request.form["department"]
        marks = request.form["marks"]
        attendance = request.form["attendance"]
        cgpa = request.form["cgpa"]

        cursor.execute("""
        UPDATE students
        SET
            name=?,
            department=?,
            marks=?,
            attendance=?,
            cgpa=?
        WHERE student_id=?
        """, (name, department, marks, attendance, cgpa, student_id))

        connection.commit()
        connection.close()

        return redirect(url_for("students"))

    cursor.execute("""
    SELECT * FROM students
    WHERE student_id=?
    """, (student_id,))

    student = cursor.fetchone()

    connection.close()

    return render_template("edit_student.html", student=student)

@app.route("/edit", methods=["GET", "POST"])
def edit():

    if "student_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    if request.method == "POST":

        department = request.form["department"]

        cursor.execute("""
        UPDATE students
        SET department=?
        WHERE student_id=?
        """, (department, session["student_id"]))

        connection.commit()

        connection.close()

        return redirect(url_for("dashboard"))

    # GET request - fetch current student details
    cursor.execute("""
    SELECT * FROM students
    WHERE student_id=?
    """, (session["student_id"],))

    student = cursor.fetchone()

    connection.close()

    return render_template("edit.html", student=student)

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        student_id = int(request.form["student_id"])
        marks = int(request.form["marks"])

        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        cursor.execute("""
        UPDATE students
        SET marks=?
        WHERE student_id=?
        """, (marks, student_id))

        if cursor.rowcount == 0:
            connection.close()
            return "❌ Student ID not found!"

        connection.commit()
        connection.close()

        return "✅ Marks Updated Successfully!"

    return render_template("admin.html")

@app.route("/students")
def students():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM students
    """)

    students = cursor.fetchall()

    connection.close()

    return render_template("students.html", students=students)

@app.route("/delete/<int:student_id>")
def delete(student_id):

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM students
    WHERE student_id=?
    """, (student_id,))

    connection.commit()
    connection.close()

    return redirect(url_for("students"))

@app.route("/search", methods=["GET", "POST"])
def search():

    student = None

    if request.method == "POST":

        student_id = request.form["student_id"]

        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM students
        WHERE student_id=?
        """, (student_id,))

        student = cursor.fetchone()

        connection.close()

    return render_template("search.html", student=student)

@app.route("/rank")
def rank():

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM students
    ORDER BY cgpa DESC
    """)

    students = cursor.fetchall()

    connection.close()

    return render_template("rank.html", students=students)

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["admin"] = True

            return redirect(url_for("admin_dashboard"))

        else:

            return "❌ Invalid Admin Username or Password"

    return render_template("admin_login.html")

@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    return render_template("admin_dashboard.html")


@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        student_id = request.form["student_id"]
        name = request.form["name"]
        department = request.form["department"]
        password = request.form["password"]

        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO students
        (student_id, name, department, password, marks, attendance, cgpa)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (student_id, name, department, password, 0, 0, 0))

        connection.commit()
        connection.close()

        return redirect(url_for("students"))

    return render_template("add_student.html")


@app.route("/report")
def report():

    if "student_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM students
    WHERE student_id=?
    """, (session["student_id"],))

    student = cursor.fetchone()

    connection.close()

    return render_template("report.html", student=student)

@app.route("/download_report")
def download_report():

    if "student_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM students
    WHERE student_id=?
    """, (session["student_id"],))

    student = cursor.fetchone()

    connection.close()

    pdf_name = f"{student[1]}_Report.pdf"

    doc = SimpleDocTemplate(pdf_name)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Student Report Card</b>", styles["Heading1"]))
    story.append(Paragraph(f"Student ID : {student[0]}", styles["Normal"]))
    story.append(Paragraph(f"Name : {student[1]}", styles["Normal"]))
    story.append(Paragraph(f"Department : {student[2]}", styles["Normal"]))
    story.append(Paragraph(f"Marks : {student[4]}", styles["Normal"]))
    story.append(Paragraph(f"Attendance : {student[5]}%", styles["Normal"]))
    story.append(Paragraph(f"CGPA : {student[6]}", styles["Normal"]))

    result = "PASS" if student[4] >= 50 else "FAIL"
    story.append(Paragraph(f"Result : {result}", styles["Normal"]))

    doc.build(story)

    return send_file(pdf_name, as_attachment=True)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)