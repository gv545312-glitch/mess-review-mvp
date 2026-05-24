from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

DATABASE = Path(__file__).parent / "reviews.db"


# ---------------- DATABASE ---------------- #

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


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


def get_all_reviews():
    conn = get_db_connection()

    reviews = conn.execute(
        "SELECT * FROM reviews ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return reviews


# ---------------- UNIVERSITIES ---------------- #

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
        "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a"
    },
    {
        "name": "Bennett University",
        "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f"
    },
    {
        "name": "JIMS Noida",
        "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d"
    }
]


# ---------------- ROUTES ---------------- #

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        university_name = request.form.get("university_name", "").strip()
        rating = request.form.get("rating", "").strip()
        feedback = request.form.get("feedback", "").strip()

        errors = []

        if not university_name:
            errors.append("Please enter your university name.")

        if rating not in {"1", "2", "3", "4", "5"}:
            errors.append("Please select rating.")

        if not feedback:
            errors.append("Please enter feedback.")

        if errors:
            return render_template(
                "index.html",
                reviews=get_all_reviews(),
                errors=errors,
                form={
                    "university_name": university_name,
                    "rating": rating,
                    "feedback": feedback,
                },
                universities=universities
            )

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO reviews
            (university_name, rating, feedback, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                university_name,
                int(rating),
                feedback,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            )
        )

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template(
        "index.html",
        reviews=get_all_reviews(),
        errors=[],
        form={},
        universities=universities
    )


# ---------------- START ---------------- #

init_db()

if __name__ == "__main__":
    app.run(debug=True)