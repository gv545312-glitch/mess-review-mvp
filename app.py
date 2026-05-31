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
    food_quality INTEGER,
    hygiene INTEGER,
    value_for_money INTEGER,
    menu_variety INTEGER,
    feedback TEXT,
    created_at TEXT
)
""")

# Add new columns if they don't exist (for existing databases)
try:
    conn.execute("ALTER TABLE reviews ADD COLUMN food_quality INTEGER DEFAULT 0")
except:
    pass
try:
    conn.execute("ALTER TABLE reviews ADD COLUMN hygiene INTEGER DEFAULT 0")
except:
    pass
try:
    conn.execute("ALTER TABLE reviews ADD COLUMN value_for_money INTEGER DEFAULT 0")
except:
    pass
try:
    conn.execute("ALTER TABLE reviews ADD COLUMN menu_variety INTEGER DEFAULT 0")
except:
    pass

conn.commit()
conn.close()


# UNIVERSITIES DATA

universities = [
    {"name": "Amity University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Lovely Professional University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Chandigarh University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Galgotias University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "SRM University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Bennett University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIT Delhi", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "IIT Bombay", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIT Madras", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIT Kanpur", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIT Kharagpur", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIT Roorkee", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIT Guwahati", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIT Hyderabad", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "NIT Trichy", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "NIT Warangal", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "NIT Surathkal", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "NIT Calicut", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "NIT Rourkela", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "BITS Pilani", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "BITS Goa", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "BITS Hyderabad", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "VIT Vellore", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "VIT Chennai", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Manipal University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Symbiosis International University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Christ University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Thapar University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Chitkara University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Delhi University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Jawaharlal Nehru University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Banaras Hindu University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Aligarh Muslim University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Hyderabad University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Jadavpur University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Anna University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Pune University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Mumbai University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Calcutta University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Panjab University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Lucknow University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Allahabad University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "IIM Ahmedabad", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIM Bangalore", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIM Calcutta", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIM Lucknow", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "IIIT Hyderabad", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIIT Delhi", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIIT Bangalore", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Amrita Vishwa Vidyapeetham", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "KL University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Gitam University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Andhra University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "JNTU Hyderabad", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Bangalore University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Visvesvaraya Technological University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Kerala University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Calicut University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Cochin University of Science and Technology", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "APJ Abdul Kalam Technological University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Savitribai Phule Pune University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Shivaji University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Nagpur University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Devi Ahilya Vishwavidyalaya", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Barkatullah University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Jiwaji University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Mohanlal Sukhadia University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Rajasthan University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Guru Nanak Dev University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Punjabi University Patiala", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "MDU Rohtak", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Kurukshetra University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "AKTU Lucknow", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "BHU Varanasi", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Ranchi University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Utkal University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Gauhati University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Goa University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Pondicherry University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IGNOU", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Jamia Millia Islamia", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "IP University Delhi", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Sharda University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Noida International University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "GLA University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Graphic Era University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "UPES Dehradun", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Nirma University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "SASTRA University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Bharathidasan University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Bharathiar University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Alagappa University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Annamalai University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Kalinga Institute of Industrial Technology", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "BIT Mesra", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Tezpur University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Assam University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
]


# HOME PAGE

@app.route("/")
def home():
    conn = get_db_connection()
    reviews = conn.execute("SELECT * FROM reviews ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", universities=universities, reviews=reviews)


# UNIVERSITY PAGE

@app.route("/university/<name>", methods=["GET", "POST"])
def university(name):
    conn = get_db_connection()

    if request.method == "POST":
        rating = int(request.form["rating"])
        food_quality = int(request.form.get("food_quality", rating))
        hygiene = int(request.form.get("hygiene", rating))
        value_for_money = int(request.form.get("value_for_money", rating))
        menu_variety = int(request.form.get("menu_variety", rating))
        feedback = request.form["feedback"]

        conn.execute("""
            INSERT INTO reviews
            (university_name, rating, food_quality, hygiene, value_for_money, menu_variety, feedback, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, rating, food_quality, hygiene, value_for_money, menu_variety, feedback, datetime.now().strftime("%d %b %Y")))
        conn.commit()
        return redirect(f"/university/{name}")

    reviews = conn.execute("""
        SELECT * FROM reviews WHERE university_name = ? ORDER BY id DESC
    """, (name,)).fetchall()
    conn.close()

    # Calculate all averages
    if reviews:
        avg_rating = round(sum(r["rating"] for r in reviews) / len(reviews), 1)
        avg_food = round(sum((r["food_quality"] or r["rating"]) for r in reviews) / len(reviews), 1)
        avg_hygiene = round(sum((r["hygiene"] or r["rating"]) for r in reviews) / len(reviews), 1)
        avg_value = round(sum((r["value_for_money"] or r["rating"]) for r in reviews) / len(reviews), 1)
        avg_variety = round(sum((r["menu_variety"] or r["rating"]) for r in reviews) / len(reviews), 1)
    else:
        avg_rating = avg_food = avg_hygiene = avg_value = avg_variety = 0

    return render_template(
        "university.html",
        university_name=name,
        reviews=reviews,
        avg_rating=avg_rating,
        avg_food=avg_food,
        avg_hygiene=avg_hygiene,
        avg_value=avg_value,
        avg_variety=avg_variety
    )


# UNIVERSITIES PAGE

@app.route("/universities")
def universities_page():
    return render_template("universities.html", universities=universities)


# RUN

if __name__ == "__main__":
    app.run(debug=True)