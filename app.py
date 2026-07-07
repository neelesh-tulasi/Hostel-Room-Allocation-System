from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "hostel_secret_key"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        rollno = request.form["rollno"]
        department = request.form["department"]
        year = request.form["year"]
        gender = request.form["gender"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        conn = sqlite3.connect("hostel.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students
            (name, rollno, department, year, gender, email, phone, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, rollno, department, year, gender, email, phone, password))

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("hostel.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, rollno, department, year, gender, email, phone
            FROM students
            WHERE email=? AND password=?
        """, (email, password))

        student = cursor.fetchone()

        conn.close()

        if student:
            session["email"] = email
            return render_template(
                "dashboard.html",
                name=student[0],
                rollno=student[1],
                department=student[2],
                year=student[3],
                gender=student[4],
                email=student[5],
                phone=student[6]
            )
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
