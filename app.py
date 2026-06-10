from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "messreview_secret_key_2026"


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

try:
    conn.execute("ALTER TABLE reviews ADD COLUMN food_quality INTEGER DEFAULT 0")
except: pass
try:
    conn.execute("ALTER TABLE reviews ADD COLUMN hygiene INTEGER DEFAULT 0")
except: pass
try:
    conn.execute("ALTER TABLE reviews ADD COLUMN value_for_money INTEGER DEFAULT 0")
except: pass
try:
    conn.execute("ALTER TABLE reviews ADD COLUMN menu_variety INTEGER DEFAULT 0")
except: pass

conn.commit()
conn.close()


# UNIVERSITIES DATA

universities = [
    {"name": "Amity University", "city": "Noida, UP", "image": "/static/images/amity.jpg"},
    {"name": "Lovely Professional University", "city": "Phagwara, Punjab", "image": "/static/images/lpu.jpg"},
    {"name": "Chandigarh University", "city": "Mohali, Punjab", "image": "/static/images/cu.jpg"},
    {"name": "Galgotias University", "city": "Greater Noida, UP", "image": "/static/images/galgotias.jpg"},
    {"name": "SRM University", "city": "Chennai, Tamil Nadu", "image": "/static/images/srm.jpg"},
    {"name": "Bennett University", "city": "Greater Noida, UP", "image": "/static/images/bennett.jpg"},
    {"name": "IIT Delhi", "city": "New Delhi", "image": "/static/images/iit_delhi.jpg"},
    {"name": "IIT Bombay", "city": "Mumbai, Maharashtra", "image": "/static/images/iit_bombay.jpg"},
    {"name": "IIT Madras", "city": "Chennai, Tamil Nadu", "image": "/static/images/iit_madras.jpg"},
    {"name": "IIT Kanpur", "city": "Kanpur, UP", "image": "/static/images/iit_kanpur.jpg"},
    {"name": "IIT Kharagpur", "city": "Kharagpur, West Bengal", "image": "/static/images/iit_kharagpur.jpg"},
    {"name": "IIT Roorkee", "city": "Roorkee, Uttarakhand", "image": "/static/images/iit_roorkee.jpg"},
    {"name": "IIT Guwahati", "city": "Guwahati, Assam", "image": "/static/images/iit_guwahati.jpg"},
    {"name": "IIT Hyderabad", "city": "Hyderabad, Telangana", "image": "/static/images/iit_hyderabad.jpg"},
    {"name": "IIT Bhubaneswar", "city": "Bhubaneswar, Odisha", "image": "https://images.unsplash.com/photo-1544531585-9847b68c8c86?w=800"},
    {"name": "IIT Gandhinagar", "city": "Gandhinagar, Gujarat", "image": "https://images.unsplash.com/photo-1508193638397-1c4234db14d8?w=800"},
    {"name": "IIT Jodhpur", "city": "Jodhpur, Rajasthan", "image": "/static/images/iit_jodhpur.jpg"},
    {"name": "IIT Mandi", "city": "Mandi, Himachal Pradesh", "image": "/static/images/iit_mandi.jpg"},
    {"name": "IIT Patna", "city": "Patna, Bihar", "image": "/static/images/iit_patna.jpg"},
    {"name": "IIT Ropar", "city": "Rupnagar, Punjab", "image": "/static/images/iit_ropar.jpg"},
    {"name": "IIT Tirupati", "city": "Tirupati, Andhra Pradesh", "image": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800"},
    {"name": "IIT Palakkad", "city": "Palakkad, Kerala", "image": "https://images.unsplash.com/photo-1513258496099-48168024aec0?w=800"},
    {"name": "IIT Dharwad", "city": "Dharwad, Karnataka", "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=800"},
    {"name": "IIT Jammu", "city": "Jammu, J&K", "image": "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?w=800"},
    {"name": "IIT Bhilai", "city": "Bhilai, Chhattisgarh", "image": "https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=800"},
    {"name": "NIT Trichy", "city": "Tiruchirappalli, Tamil Nadu", "image": "/static/images/nit_trichy.jpg"},
    {"name": "NIT Warangal", "city": "Warangal, Telangana", "image": "/static/images/nit_warangal.jpg"},
    {"name": "NIT Surathkal", "city": "Mangalore, Karnataka", "image": "/static/images/nit_surathkal.jpg"},
    {"name": "NIT Calicut", "city": "Kozhikode, Kerala", "image": "/static/images/nit_calicut.jpg"},
    {"name": "NIT Rourkela", "city": "Rourkela, Odisha", "image": "/static/images/nit_rourkela.jpg"},
    {"name": "NIT Allahabad", "city": "Prayagraj, UP", "image": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800"},
    {"name": "NIT Jaipur", "city": "Jaipur, Rajasthan", "image": "/static/images/nit_jaipur.jpg"},
    {"name": "NIT Kurukshetra", "city": "Kurukshetra, Haryana", "image": "/static/images/nit_kurukshetra.jpg"},
    {"name": "NIT Durgapur", "city": "Durgapur, West Bengal", "image": "/static/images/nit_durgapur.jpg"},
    {"name": "NIT Surat", "city": "Surat, Gujarat", "image": "https://images.unsplash.com/photo-1532619675605-1ede6c2ed2b0?w=800"},
    {"name": "NIT Hamirpur", "city": "Hamirpur, Himachal Pradesh", "image": "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800"},
    {"name": "NIT Jalandhar", "city": "Jalandhar, Punjab", "image": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800"},
    {"name": "NIT Nagpur", "city": "Nagpur, Maharashtra", "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800"},
    {"name": "NIT Patna", "city": "Patna, Bihar", "image": "https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=800"},
    {"name": "NIT Silchar", "city": "Silchar, Assam", "image": "/static/images/nit_silchar.jpg"},
    {"name": "NIT Agartala", "city": "Agartala, Tripura", "image": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=800"},
    {"name": "NIT Manipur", "city": "Imphal, Manipur", "image": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800"},
    {"name": "NIT Meghalaya", "city": "Shillong, Meghalaya", "image": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=800"},
    {"name": "NIT Mizoram", "city": "Aizawl, Mizoram", "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800"},
    {"name": "NIT Goa", "city": "Goa", "image": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800"},
    {"name": "NIT Puducherry", "city": "Puducherry", "image": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800"},
    {"name": "NIT Sikkim", "city": "Gangtok, Sikkim", "image": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800"},
    {"name": "NIT Uttarakhand", "city": "Srinagar, Uttarakhand", "image": "https://images.unsplash.com/photo-1573164713988-8665fc963095?w=800"},
    {"name": "BITS Pilani", "city": "Pilani, Rajasthan", "image": "/static/images/bits_pilani.jpg"},
    {"name": "BITS Goa", "city": "Goa", "image": "/static/images/bits_goa.jpg"},
    {"name": "BITS Hyderabad", "city": "Hyderabad, Telangana", "image": "/static/images/bits_hyderabad.jpg"},
    {"name": "VIT Vellore", "city": "Vellore, Tamil Nadu", "image": "/static/images/vit_vellore.jpg"},
    {"name": "VIT Chennai", "city": "Chennai, Tamil Nadu", "image": "/static/images/vit_chennai.jpg"},
    {"name": "VIT Bhopal", "city": "Bhopal, MP", "image": "/static/images/vit_bhopal.jpg"},
    {"name": "VIT AP", "city": "Amaravati, Andhra Pradesh", "image": "/static/images/vit_ap.jpg"},
    {"name": "Manipal University", "city": "Manipal, Karnataka", "image": "/static/images/manipal.jpg"},
    {"name": "Manipal University Jaipur", "city": "Jaipur, Rajasthan", "image": "/static/images/manipal_jaipur.jpg"},
    {"name": "Symbiosis International University", "city": "Pune, Maharashtra", "image": "/static/images/symbiosis.jpg"},
    {"name": "Christ University", "city": "Bangalore, Karnataka", "image": "/static/images/christ_university.jpg"},
    {"name": "Thapar University", "city": "Patiala, Punjab", "image": "/static/images/thapar.jpg"},
    {"name": "Chitkara University", "city": "Rajpura, Punjab", "image": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=800"},
    {"name": "Graphic Era University", "city": "Dehradun, Uttarakhand", "image": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800"},
    {"name": "UPES Dehradun", "city": "Dehradun, Uttarakhand", "image": "https://images.unsplash.com/photo-1530099486328-e021101a494a?w=800"},
    {"name": "Nirma University", "city": "Ahmedabad, Gujarat", "image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=800"},
    {"name": "Kalinga Institute of Industrial Technology", "city": "Bhubaneswar, Odisha", "image": "/static/images/kiit.jpg"},
    {"name": "Delhi University", "city": "New Delhi", "image": "/static/images/du.jpg"},
    {"name": "Jawaharlal Nehru University", "city": "New Delhi", "image": "/static/images/jnu.jpg"},
    {"name": "Banaras Hindu University", "city": "Varanasi, UP", "image": "/static/images/bhu.jpg"},
    {"name": "Aligarh Muslim University", "city": "Aligarh, UP", "image": "/static/images/amu.jpg"},
    {"name": "Hyderabad University", "city": "Hyderabad, Telangana", "image": "/static/images/hyderabad_university.jpg"},
    {"name": "Jadavpur University", "city": "Kolkata, West Bengal", "image": "/static/images/jadavpur.jpg"},
    {"name": "Anna University", "city": "Chennai, Tamil Nadu", "image": "/static/images/anna_university.jpg"},
    {"name": "Mumbai University", "city": "Mumbai, Maharashtra", "image": "/static/images/mumbai_university.jpg"},
    {"name": "Calcutta University", "city": "Kolkata, West Bengal", "image": "/static/images/calcutta_university.jpg"},
    {"name": "Panjab University", "city": "Chandigarh", "image": "/static/images/panjab_university.jpg"},
    {"name": "Lucknow University", "city": "Lucknow, UP", "image": "/static/images/lucknow_university.jpg"},
    {"name": "Allahabad University", "city": "Prayagraj, UP", "image": "/static/images/allahabad_university.jpg"},
    {"name": "Patna University", "city": "Patna, Bihar", "image": "https://images.unsplash.com/photo-1604872440371-a1a45d2c7ce4?w=800"},
    {"name": "Gauhati University", "city": "Guwahati, Assam", "image": "/static/images/gauhati_university.jpg"},
    {"name": "Jammu University", "city": "Jammu, J&K", "image": "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=800"},
    {"name": "Kashmir University", "city": "Srinagar, J&K", "image": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=800"},
    {"name": "Manipur University", "city": "Imphal, Manipur", "image": "https://images.unsplash.com/photo-1577896851231-70ef18881754?w=800"},
    {"name": "Sikkim University", "city": "Gangtok, Sikkim", "image": "https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=800"},
    {"name": "Tripura University", "city": "Agartala, Tripura", "image": "https://images.unsplash.com/photo-1520531158340-44015069e78e?w=800"},
    {"name": "Mizoram University", "city": "Aizawl, Mizoram", "image": "https://images.unsplash.com/photo-1526256262350-7da7584cf5eb?w=800"},
    {"name": "Assam University", "city": "Silchar, Assam", "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800"},
    {"name": "Tezpur University", "city": "Tezpur, Assam", "image": "https://images.unsplash.com/photo-1531545514256-b1400bc00f31?w=800"},
    {"name": "IIM Ahmedabad", "city": "Ahmedabad, Gujarat", "image": "/static/images/iim_ahmedabad.jpg"},
    {"name": "IIM Bangalore", "city": "Bangalore, Karnataka", "image": "/static/images/iim_bangalore.jpg"},
    {"name": "IIM Calcutta", "city": "Kolkata, West Bengal", "image": "/static/images/iim_calcutta.jpg"},
    {"name": "IIM Lucknow", "city": "Lucknow, UP", "image": "/static/images/iim_lucknow.jpg"},
    {"name": "IIM Kozhikode", "city": "Kozhikode, Kerala", "image": "/static/images/iim_kozhikode.jpg"},
    {"name": "IIM Indore", "city": "Indore, MP", "image": "/static/images/iim_indore.jpg"},
    {"name": "IIM Shillong", "city": "Shillong, Meghalaya", "image": "/static/images/iim_shillong.jpg"},
    {"name": "IIM Rohtak", "city": "Rohtak, Haryana", "image": "/static/images/iim_rohtak.jpg"},
    {"name": "IIM Ranchi", "city": "Ranchi, Jharkhand", "image": "/static/images/iim_ranchi.jpg"},
    {"name": "IIM Raipur", "city": "Raipur, Chhattisgarh", "image": "/static/images/iim_raipur.jpg"},
    {"name": "IIM Trichy", "city": "Tiruchirappalli, Tamil Nadu", "image": "https://images.unsplash.com/photo-1531973576160-7125cd663d86?w=800"},
    {"name": "IIM Udaipur", "city": "Udaipur, Rajasthan", "image": "/static/images/iim_udaipur.jpg"},
    {"name": "IIM Nagpur", "city": "Nagpur, Maharashtra", "image": "/static/images/iim_nagpur.jpg"},
    {"name": "IIM Jammu", "city": "Jammu, J&K", "image": "/static/images/iim_jammu.jpg"},
    {"name": "IIIT Hyderabad", "city": "Hyderabad, Telangana", "image": "/static/images/iiit_hyderabad.jpg"},
    {"name": "IIIT Delhi", "city": "New Delhi", "image": "/static/images/iiit_delhi.jpg"},
    {"name": "IIIT Bangalore", "city": "Bangalore, Karnataka", "image": "/static/images/iiit_bangalore.jpg"},
    {"name": "IIIT Allahabad", "city": "Prayagraj, UP", "image": "/static/images/iiit_allahabad.jpg"},
    {"name": "IIIT Gwalior", "city": "Gwalior, MP", "image": "/static/images/iiit_gwalior.jpg"},
    {"name": "IIIT Lucknow", "city": "Lucknow, UP", "image": "/static/images/iiit_lucknow.jpg"},
    {"name": "IIIT Pune", "city": "Pune, Maharashtra", "image": "/static/images/iiit_pune.jpg"},
    {"name": "IIIT Nagpur", "city": "Nagpur, Maharashtra", "image": "/static/images/iiit_nagpur.jpg"},
    {"name": "Amrita Vishwa Vidyapeetham", "city": "Coimbatore, Tamil Nadu", "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800"},
    {"name": "KL University", "city": "Guntur, Andhra Pradesh", "image": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800"},
    {"name": "Gitam University", "city": "Visakhapatnam, AP", "image": "https://images.unsplash.com/photo-1535982330050-f1c2fb79ff84?w=800"},
    {"name": "Andhra University", "city": "Visakhapatnam, AP", "image": "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=800"},
    {"name": "JNTU Hyderabad", "city": "Hyderabad, Telangana", "image": "https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=800"},
    {"name": "Bangalore University", "city": "Bangalore, Karnataka", "image": "/static/images/bangalore_university.jpg"},
    {"name": "Visvesvaraya Technological University", "city": "Belagavi, Karnataka", "image": "/static/images/vtu.jpg"},
    {"name": "Kerala University", "city": "Thiruvananthapuram, Kerala", "image": "/static/images/kerala_university.jpg"},
    {"name": "Calicut University", "city": "Malappuram, Kerala", "image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=800"},
    {"name": "Cochin University of Science and Technology", "city": "Kochi, Kerala", "image": "/static/images/cochin_university.jpg"},
    {"name": "APJ Abdul Kalam Technological University", "city": "Thiruvananthapuram, Kerala", "image": "/static/images/apj_ktu.jpg"},
    {"name": "Savitribai Phule Pune University", "city": "Pune, Maharashtra", "image": "/static/images/pune_university.jpg"},
    {"name": "Shivaji University", "city": "Kolhapur, Maharashtra", "image": "/static/images/shivaji_university.jpg"},
    {"name": "Nagpur University", "city": "Nagpur, Maharashtra", "image": "/static/images/nagpur_university.jpg"},
    {"name": "Devi Ahilya Vishwavidyalaya", "city": "Indore, MP", "image": "/static/images/devi_ahilya.jpg"},
    {"name": "Barkatullah University", "city": "Bhopal, MP", "image": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800"},
    {"name": "Jiwaji University", "city": "Gwalior, MP", "image": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800"},
    {"name": "Mohanlal Sukhadia University", "city": "Udaipur, Rajasthan", "image": "https://images.unsplash.com/photo-1556761175-b413da4baf72?w=800"},
    {"name": "Rajasthan University", "city": "Jaipur, Rajasthan", "image": "/static/images/rajasthan_university.jpg"},
    {"name": "Guru Nanak Dev University", "city": "Amritsar, Punjab", "image": "/static/images/guru_nanak.jpg"},
    {"name": "Punjabi University Patiala", "city": "Patiala, Punjab", "image": "/static/images/punjabi_university.jpg"},
    {"name": "MDU Rohtak", "city": "Rohtak, Haryana", "image": "/static/images/mdu_rohtak.jpg"},
    {"name": "Kurukshetra University", "city": "Kurukshetra, Haryana", "image": "/static/images/kurukshetra_university.jpg"},
    {"name": "AKTU Lucknow", "city": "Lucknow, UP", "image": "https://images.unsplash.com/photo-1576495199011-eb94736d05d6?w=800"},
    {"name": "Ranchi University", "city": "Ranchi, Jharkhand", "image": "/static/images/ranchi_university.jpg"},
    {"name": "Utkal University", "city": "Bhubaneswar, Odisha", "image": "/static/images/utkal_university.jpg"},
    {"name": "Goa University", "city": "Goa", "image": "/static/images/goa_university.jpg"},
    {"name": "Pondicherry University", "city": "Puducherry", "image": "/static/images/pondicherry_university.jpg"},
    {"name": "IGNOU", "city": "New Delhi", "image": "/static/images/ignou.jpg"},
    {"name": "Jamia Millia Islamia", "city": "New Delhi", "image": "/static/images/jamia_millia.jpg"},
    {"name": "IP University Delhi", "city": "New Delhi", "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800"},
    {"name": "Sharda University", "city": "Greater Noida, UP", "image": "https://images.unsplash.com/photo-1531545514256-b1400bc00f31?w=800"},
    {"name": "GLA University", "city": "Mathura, UP", "image": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800"},
    {"name": "BIT Mesra", "city": "Ranchi, Jharkhand", "image": "https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=800"},
    {"name": "SASTRA University", "city": "Thanjavur, Tamil Nadu", "image": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=800"},
    {"name": "Bharathidasan University", "city": "Tiruchirappalli, Tamil Nadu", "image": "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=800"},
    {"name": "Bharathiar University", "city": "Coimbatore, Tamil Nadu", "image": "https://images.unsplash.com/photo-1462826303086-329426d1aef5?w=800"},
    {"name": "Alagappa University", "city": "Karaikudi, Tamil Nadu", "image": "https://images.unsplash.com/photo-1504607798333-52a30db54a5d?w=800"},
    {"name": "Annamalai University", "city": "Chidambaram, Tamil Nadu", "image": "https://images.unsplash.com/photo-1527192491265-7e15c55b1ed2?w=800"},
]


# HOME PAGE

@app.route("/")
def home():
    conn = get_db_connection()
    reviews = conn.execute("SELECT * FROM reviews ORDER BY id DESC").fetchall()

    # Real rating + review count per university
    uni_stats = {}
    for uni in universities:
        name = uni["name"]
        uni_reviews = conn.execute(
            "SELECT rating FROM reviews WHERE university_name = ?", (name,)
        ).fetchall()
        count = len(uni_reviews)
        avg = round(sum(r["rating"] for r in uni_reviews) / count, 1) if count > 0 else None
        uni_stats[name] = {"count": count, "avg": avg}

    # Top ranked — universities with reviews, sorted by avg rating
    ranked = [
        {"name": u["name"], "city": u["city"], "avg": uni_stats[u["name"]]["avg"], "count": uni_stats[u["name"]]["count"]}
        for u in universities if uni_stats[u["name"]]["avg"] is not None
    ]
    ranked.sort(key=lambda x: x["avg"], reverse=True)
    top_ranked = ranked[:5]

    # Compare top 3
    compare_unis = ranked[:3]

    conn.close()
    return render_template("index.html",
        universities=universities,
        reviews=reviews,
        uni_stats=uni_stats,
        top_ranked=top_ranked,
        compare_unis=compare_unis
    )


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

    uni = next((u for u in universities if u["name"] == name), None)
    city = uni["city"] if uni else "India"

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
        city=city,
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
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", "").lower().strip()
    per_page = 24

    # Filter by search query across ALL universities
    if q:
        filtered = [u for u in universities if q in u["name"].lower() or q in u["city"].lower()]
    else:
        filtered = universities

    total = len(filtered)
    total_pages = max(1, (total + per_page - 1) // per_page)
    page = min(page, total_pages)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = filtered[start:end]

    conn = get_db_connection()
    uni_stats = {}
    for uni in paginated:
        name = uni["name"]
        uni_reviews = conn.execute(
            "SELECT rating FROM reviews WHERE university_name = ?", (name,)
        ).fetchall()
        count = len(uni_reviews)
        avg = round(sum(r["rating"] for r in uni_reviews) / count, 1) if count > 0 else None
        uni_stats[name] = {"count": count, "avg": avg}
    conn.close()

    return render_template("universities.html",
        universities=paginated,
        uni_stats=uni_stats,
        page=page,
        total_pages=total_pages,
        total=total,
        q=q
    )




# ─── ADMIN ───────────────────────────────────────────────

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "messreview2026"

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        from flask import session, redirect
        if not session.get("admin_logged_in"):
            return redirect("/admin/login")
        return f(*args, **kwargs)
    return decorated

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    from flask import session, request
    error = None
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect("/admin")
        else:
            error = "Invalid username or password"
    return render_template("admin_login.html", error=error)

@app.route("/admin/logout")
def admin_logout():
    from flask import session
    session.pop("admin_logged_in", None)
    return redirect("/admin/login")

@app.route("/admin")
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    total_reviews = conn.execute("SELECT COUNT(*) FROM reviews").fetchone()[0]
    avg_rating = conn.execute("SELECT AVG(rating) FROM reviews").fetchone()[0]
    avg_rating = round(avg_rating, 1) if avg_rating else 0
    recent_reviews = conn.execute("SELECT * FROM reviews ORDER BY id DESC LIMIT 5").fetchall()
    conn.close()
    total_unis = len(universities)
    return render_template("admin.html", 
        page="dashboard",
        total_reviews=total_reviews,
        total_unis=total_unis,
        avg_rating=avg_rating,
        recent_reviews=recent_reviews,
        universities=universities
    )

@app.route("/admin/reviews")
@admin_required
def admin_reviews():
    conn = get_db_connection()
    uni_filter = request.args.get("uni", "")
    if uni_filter:
        reviews = conn.execute("SELECT * FROM reviews WHERE university_name = ? ORDER BY id DESC", (uni_filter,)).fetchall()
    else:
        reviews = conn.execute("SELECT * FROM reviews ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html",
        page="reviews",
        reviews=reviews,
        universities=universities,
        uni_filter=uni_filter
    )

@app.route("/admin/reviews/delete/<int:review_id>")
@admin_required
def admin_delete_review(review_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
    conn.commit()
    conn.close()
    return redirect("/admin/reviews")

@app.route("/admin/universities")
@admin_required
def admin_universities():
    return render_template("admin.html",
        page="universities",
        universities=universities
    )

@app.route("/admin/universities/add", methods=["POST"])
@admin_required
def admin_add_university():
    name = request.form["name"].strip()
    city = request.form["city"].strip()
    image = request.form["image"].strip()
    if name and city:
        if not image:
            image = "https://images.unsplash.com/photo-1562774053-701939374585?w=800"
        universities.append({"name": name, "city": city, "image": image})
    return redirect("/admin/universities")

@app.route("/admin/universities/delete/<name>")
@admin_required
def admin_delete_university(name):
    global universities
    universities = [u for u in universities if u["name"] != name]
    return redirect("/admin/universities")



# SEARCH API

@app.route("/search")
def search():
    from flask import jsonify
    q = request.args.get("q", "").lower().strip()
    if not q or len(q) < 2:
        return jsonify([])
    results = [
        {"name": u["name"], "city": u["city"], "image": u["image"]}
        for u in universities
        if q in u["name"].lower() or q in u["city"].lower()
    ][:10]
    return jsonify(results)

# RUN

if __name__ == "__main__":
    app.run(debug=True)