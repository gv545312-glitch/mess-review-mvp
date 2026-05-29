from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

DATABASE = Path(__file__).parent / "reviews.db"


# DATABASE CONNECTION

def get_db_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# CREATE TABLE

def init_db():

    conn = get_db_connection()

    conn.execute("""

        CREATE TABLE IF NOT EXISTS reviews (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            university_name TEXT NOT NULL,

            rating INTEGER NOT NULL,

            feedback TEXT NOT NULL,

            created_at TEXT NOT NULL

        )

    """)

    conn.commit()

    conn.close()


init_db()


# UNIVERSITY DATA

universities = [

    {
        "name": "Amity University",
        "image": "https://images.unsplash.com/photo-1562774053-701939374585"
    },

    {
        "name": "Galgotias University",
        "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1"
    },

    {
        "name": "Sharda University",
        "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f"
    },

    {
        "name": "Bennett University",
        "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b"
    },

    {
        "name": "JIMS Noida",
        "image": "https://images.unsplash.com/photo-1592280771190-3e2e4d571952"
    }

]


# HOME PAGE

@app.route("/", methods=["GET", "POST"])
def home():

    conn = get_db_connection()

    if request.method == "POST":

        university_name = request.form["university_name"]

        rating = request.form["rating"]

        feedback = request.form["feedback"]

        conn.execute(
            "INSERT INTO reviews (university_name, rating, feedback, created_at) VALUES (?, ?, ?, ?)",
            (
                university_name,
                rating,
                feedback,
                datetime.now().strftime("%d %b %Y %I:%M %p")
            )
        )

        conn.commit()

        return redirect("/")

    reviews = conn.execute(
        "SELECT * FROM reviews ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        universities=universities,
        reviews=reviews
    )


# UNIVERSITY PAGE

@app.route("/university/<name>", methods=["GET", "POST"])
def university_page(name):

    conn = get_db_connection()

    if request.method == "POST":

        rating = request.form["rating"]

        feedback = request.form["feedback"]

        conn.execute(
            "INSERT INTO reviews (university_name, rating, feedback, created_at) VALUES (?, ?, ?, ?)",
            (
                name,
                rating,
                feedback,
                datetime.now().strftime("%d %b %Y %I:%M %p")
            )
        )

        conn.commit()

    reviews = conn.execute(
        "SELECT * FROM reviews WHERE university_name = ? ORDER BY id DESC",
        (name,)
    ).fetchall()

    conn.close()

    return render_template(
        "university.html",
        university_name=name,
        reviews=reviews
    )


if __name__ == "__main__":

    app.run(debug=True)