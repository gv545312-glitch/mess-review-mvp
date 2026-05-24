import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

DATABASE = Path(__file__).parent / "reviews.db"


def get_db_connection():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the reviews table if it does not exist."""
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            university_name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            feedback TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def get_all_reviews():
    """Fetch all reviews, newest first."""
    conn = get_db_connection()
    reviews = conn.execute(
        "SELECT * FROM reviews ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return reviews

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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        university_name = request.form.get("university_name", "").strip()
        rating = request.form.get("rating", "").strip()
        feedback = request.form.get("feedback", "").strip()

        # Basic validation
        errors = []
        if not university_name:
            errors.append("Please enter your university name.")
        if rating not in {"1", "2", "3", "4", "5"}:
            errors.append("Please select a rating from 1 to 5.")
        if not feedback:
            errors.append("Please write your feedback.")

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
            )

        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO reviews (university_name, rating, feedback, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                university_name,
                int(rating),
                feedback,
                datetime.now().strftime("%Y-%m-%d %H:%M"),
            ),
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

init_db()

if __name__ == "__main__":
    app.run(debug=True)