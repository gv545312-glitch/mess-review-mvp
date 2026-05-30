from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)


# DATABASE

def get_db_connection():

    conn = sqlite3.connect("reviews.db")
    conn.row_factory = sqlite3.Row

    return conn


# CREATE TABLE

conn = get_db_connection()

conn.execute("""

CREATE TABLE IF NOT EXISTS reviews (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    university_name TEXT,

    rating INTEGER,

    feedback TEXT,

    created_at TEXT

)

""")

conn.commit()
conn.close()


# UNIVERSITIES DATA

universities = [

    {
        "name":"Amity University",
        "image":"https://images.unsplash.com/photo-1562774053-701939374585?w=800"
    },

    {
        "name":"Lovely Professional University",
        "image":"https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"
    },

    {
        "name":"Chandigarh University",
        "image":"https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"
    },

    {
        "name":"Galgotias University",
        "image":"https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"
    },

    {
        "name":"SRM University",
        "image":"https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"
    },

    {
        "name":"Bennett University",
        "image":"https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"
    }

]


# HOME PAGE

@app.route("/")

def home():

    conn = get_db_connection()

    reviews = conn.execute("""

        SELECT * FROM reviews
        ORDER BY id DESC

    """).fetchall()

    conn.close()

    return render_template(

        "index.html",

        universities=universities,
        reviews=reviews

    )


# UNIVERSITY PAGE

@app.route("/university/<name>", methods=["GET", "POST"])

def university(name):

    conn = get_db_connection()

    if request.method == "POST":

        rating = request.form["rating"]
        feedback = request.form["feedback"]

        conn.execute("""

            INSERT INTO reviews
            (
                university_name,
                rating,
                feedback,
                created_at
            )

            VALUES (?, ?, ?, ?)

        """, (

            name,
            rating,
            feedback,
            datetime.now().strftime("%d %b %Y")

        ))

        conn.commit()

        return redirect(f"/university/{name}")



    reviews = conn.execute("""

        SELECT * FROM reviews

        WHERE university_name = ?

        ORDER BY id DESC

    """, (name,)).fetchall()

    conn.close()

    return render_template(

        "university.html",

        university_name=name,
        reviews=reviews

    )


# UNIVERSITIES PAGE

@app.route("/universities")

def universities_page():

    return render_template(

        "universities.html",

        universities=universities

    )


# RUN

if __name__ == "__main__":

    app.run(debug=True)