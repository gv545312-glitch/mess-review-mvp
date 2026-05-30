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

# Real Indian Universities List - paste this in app.py replacing the universities = [...] list

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
    {"name": "IIT Bhubaneswar", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIT Gandhinagar", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIT Jodhpur", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIT Mandi", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIT Patna", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIT Ropar", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIT Tirupati", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "IIT Palakkad", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIT Dharwad", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIT Jammu", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIT Bhilai", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "NIT Trichy", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "NIT Warangal", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "NIT Surathkal", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "NIT Calicut", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "NIT Rourkela", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "NIT Allahabad", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "NIT Jaipur", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "NIT Kurukshetra", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "NIT Durgapur", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "NIT Surat", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "NIT Hamirpur", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "NIT Jalandhar", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "NIT Nagpur", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "NIT Patna", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "NIT Silchar", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "NIT Agartala", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "NIT Arunachal Pradesh", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "NIT Manipur", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "NIT Meghalaya", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "NIT Mizoram", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "NIT Nagaland", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "NIT Puducherry", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "NIT Sikkim", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "NIT Uttarakhand", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "NIT Goa", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
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
    {"name": "Madras University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Osmania University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Mysore University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Gujarat University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Rajasthan University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Panjab University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Lucknow University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Allahabad University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Patna University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Gauhati University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Jammu University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Kashmir University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Manipur University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Nagaland University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Sikkim University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Tripura University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Mizoram University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Assam University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Dibrugarh University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Tezpur University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "BITS Pilani", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "BITS Goa", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "BITS Hyderabad", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "VIT Vellore", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "VIT Chennai", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "VIT Bhopal", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "VIT AP", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Manipal University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Manipal University Jaipur", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Manipal University Bhubaneswar", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Symbiosis International University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Christ University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Presidency University Bangalore", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Shoolini University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Thapar University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Chitkara University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Graphic Era University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Uttaranchal University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "DIT University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Quantum University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Sharda University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Noida International University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "GLA University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Invertis University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Teerthanker Mahaveer University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Integral University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Rama University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Shri Ramswaroop Memorial University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Babu Banarasi Das University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIIT Hyderabad", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIIT Bangalore", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIIT Delhi", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "IIIT Allahabad", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIIT Gwalior", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIIT Jabalpur", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIIT Kancheepuram", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIIT Pune", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIIT Vadodara", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIIT Ranchi", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "IIIT Lucknow", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIIT Dharwad", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIIT Kottayam", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIIT Una", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIIT Sri City", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIIT Sonepat", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIIT Kalyani", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "IIIT Nagpur", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIIT Bhopal", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIIT Agartala", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIM Ahmedabad", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIM Bangalore", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIM Calcutta", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIM Lucknow", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "IIM Kozhikode", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIM Indore", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIM Shillong", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIM Rohtak", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIM Ranchi", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIM Raipur", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIM Trichy", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "IIM Udaipur", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIM Kashipur", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIM Nagpur", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIM Visakhapatnam", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIM Bodh Gaya", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIM Sirmaur", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIM Sambalpur", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "IIM Jammu", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Jadavpur University Kolkata", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "PSG College of Technology", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Coimbatore Institute of Technology", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "College of Engineering Pune", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "VJTI Mumbai", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "SGSITS Indore", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "BIT Mesra", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "DAIICT Gandhinagar", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "LNMIIT Jaipur", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "PEC Chandigarh", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Tezpur University Assam", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "PDPU Gandhinagar", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "UPES Dehradun", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Nirma University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Dhirubhai Ambani Institute", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Kalinga Institute of Industrial Technology", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "SRM Institute of Science and Technology", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Saveetha University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "SASTRA University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Karunya University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Kongu Engineering College", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Amrita Vishwa Vidyapeetham", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "KL University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Gitam University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Vignan University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Andhra University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Sri Venkateswara University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "JNTU Hyderabad", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "JNTU Kakinada", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "JNTU Anantapur", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Bangalore University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Visvesvaraya Technological University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Mangalore University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Kuvempu University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Gulbarga University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Davangere University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Rani Channamma University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Tumkur University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Periyar University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Bharathidasan University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Bharathiar University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Alagappa University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Annamalai University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Mother Teresa Women's University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Kerala University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Calicut University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Cochin University of Science and Technology", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Mahatma Gandhi University Kerala", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Kannur University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "APJ Abdul Kalam Technological University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Savitribai Phule Pune University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Shivaji University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "North Maharashtra University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "SNDT Women's University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Dr Babasaheb Ambedkar Marathwada University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Rashtrasant Tukadoji Maharaj Nagpur University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Swami Ramanand Teerth Marathwada University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Gondwana University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Sant Gadge Baba Amravati University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Solapur University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Hemchand Yadav Vishwavidyalaya", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Pt Ravishankar Shukla University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Devi Ahilya Vishwavidyalaya", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Barkatullah University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Vikram University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Jiwaji University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Awadhesh Pratap Singh University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Maharishi Mahesh Yogi Vedic University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Mohanlal Sukhadia University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Jai Narain Vyas University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "MDS University Ajmer", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Kota University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Brij University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Shekhawati University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Guru Nanak Dev University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Punjabi University Patiala", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Guru Gobind Singh Indraprastha University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "MDU Rohtak", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Kurukshetra University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Chaudhary Charan Singh University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "AKTU Lucknow", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "CSJMU Kanpur", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "DDU Gorakhpur University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "MG Kashi Vidyapith", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Sampurnanand Sanskrit University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Veer Bahadur Singh PU Jaunpur", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Bundelkhand University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Magadh University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Lalit Narayan Mithila University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Veer Kunwar Singh University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "BR Ambedkar Bihar University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Ranchi University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Vinoba Bhave University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Kolhan University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Sido Kanhu Murmu University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Utkal University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Berhampur University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Sambalpur University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "North Orissa University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Fakir Mohan University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Rabindra Bharati University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Vidyasagar University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Burdwan University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "North Bengal University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "Kalyani University", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Goa University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Pondicherry University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IGNOU", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Jamia Millia Islamia", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Jamia Hamdard", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Dr BR Ambedkar University Delhi", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "IP University Delhi", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Indira Gandhi National Tribal University", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Nalanda University", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Rajiv Gandhi University", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Hemwati Nandan Bahuguna Garhwal University", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Kumaun University", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Doon University", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
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
            INSERT INTO reviews (university_name, rating, feedback, created_at)
            VALUES (?, ?, ?, ?)
        """, (name, rating, feedback, datetime.now().strftime("%d %b %Y")))
        conn.commit()
        return redirect(f"/university/{name}")

    reviews = conn.execute("""
        SELECT * FROM reviews
        WHERE university_name = ?
        ORDER BY id DESC
    """, (name,)).fetchall()

    conn.close()

    # Average rating calculate karo
    if reviews:
        avg_rating = round(sum(r["rating"] for r in reviews) / len(reviews), 1)
    else:
        avg_rating = 0

    return render_template(
        "university.html",
        university_name=name,
        reviews=reviews,
        avg_rating=avg_rating
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