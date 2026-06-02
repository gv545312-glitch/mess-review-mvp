from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from urllib.parse import quote_plus, quote
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json

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
    {"name": "Amity University", "city": "Noida, UP", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Lovely Professional University", "city": "Phagwara, Punjab", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Chandigarh University", "city": "Mohali, Punjab", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Galgotias University", "city": "Greater Noida, UP", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "SRM University", "city": "Chennai, Tamil Nadu", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Bennett University", "city": "Greater Noida, UP", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIT Delhi", "city": "New Delhi", "image": "https://images.unsplash.com/photo-1592280771190-3e2e4d571952?w=800"},
    {"name": "IIT Bombay", "city": "Mumbai, Maharashtra", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIT Madras", "city": "Chennai, Tamil Nadu", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIT Kanpur", "city": "Kanpur, UP", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIT Kharagpur", "city": "Kharagpur, West Bengal", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIT Roorkee", "city": "Roorkee, Uttarakhand", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIT Guwahati", "city": "Guwahati, Assam", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIT Hyderabad", "city": "Hyderabad, Telangana", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIT Bhubaneswar", "city": "Bhubaneswar, Odisha", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIT Gandhinagar", "city": "Gandhinagar, Gujarat", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIT Jodhpur", "city": "Jodhpur, Rajasthan", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIT Mandi", "city": "Mandi, Himachal Pradesh", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIT Patna", "city": "Patna, Bihar", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIT Ropar", "city": "Rupnagar, Punjab", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIT Tirupati", "city": "Tirupati, Andhra Pradesh", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIT Palakkad", "city": "Palakkad, Kerala", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIT Dharwad", "city": "Dharwad, Karnataka", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIT Jammu", "city": "Jammu, J&K", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIT Bhilai", "city": "Bhilai, Chhattisgarh", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "NIT Trichy", "city": "Tiruchirappalli, Tamil Nadu", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "NIT Warangal", "city": "Warangal, Telangana", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "NIT Surathkal", "city": "Mangalore, Karnataka", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "NIT Calicut", "city": "Kozhikode, Kerala", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "NIT Rourkela", "city": "Rourkela, Odisha", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "NIT Allahabad", "city": "Prayagraj, UP", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "NIT Jaipur", "city": "Jaipur, Rajasthan", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "NIT Kurukshetra", "city": "Kurukshetra, Haryana", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "NIT Durgapur", "city": "Durgapur, West Bengal", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "NIT Surat", "city": "Surat, Gujarat", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "NIT Hamirpur", "city": "Hamirpur, Himachal Pradesh", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "NIT Jalandhar", "city": "Jalandhar, Punjab", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "NIT Nagpur", "city": "Nagpur, Maharashtra", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "NIT Patna", "city": "Patna, Bihar", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "NIT Silchar", "city": "Silchar, Assam", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "NIT Agartala", "city": "Agartala, Tripura", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "NIT Manipur", "city": "Imphal, Manipur", "image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"},
    {"name": "NIT Meghalaya", "city": "Shillong, Meghalaya", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "NIT Mizoram", "city": "Aizawl, Mizoram", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "NIT Goa", "city": "Goa", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "NIT Puducherry", "city": "Puducherry", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "NIT Sikkim", "city": "Gangtok, Sikkim", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "NIT Uttarakhand", "city": "Srinagar, Uttarakhand", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "BITS Pilani", "city": "Pilani, Rajasthan", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "BITS Goa", "city": "Goa", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "BITS Hyderabad", "city": "Hyderabad, Telangana", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "VIT Vellore", "city": "Vellore, Tamil Nadu", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "VIT Chennai", "city": "Chennai, Tamil Nadu", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "VIT Bhopal", "city": "Bhopal, MP", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "VIT AP", "city": "Amaravati, Andhra Pradesh", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Manipal University", "city": "Manipal, Karnataka", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Manipal University Jaipur", "city": "Jaipur, Rajasthan", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Symbiosis International University", "city": "Pune, Maharashtra", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Christ University", "city": "Bangalore, Karnataka", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Thapar University", "city": "Patiala, Punjab", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Chitkara University", "city": "Rajpura, Punjab", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Graphic Era University", "city": "Dehradun, Uttarakhand", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "UPES Dehradun", "city": "Dehradun, Uttarakhand", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Nirma University", "city": "Ahmedabad, Gujarat", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Kalinga Institute of Industrial Technology", "city": "Bhubaneswar, Odisha", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Delhi University", "city": "New Delhi", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Jawaharlal Nehru University", "city": "New Delhi", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Banaras Hindu University", "city": "Varanasi, UP", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Aligarh Muslim University", "city": "Aligarh, UP", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Hyderabad University", "city": "Hyderabad, Telangana", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Jadavpur University", "city": "Kolkata, West Bengal", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Anna University", "city": "Chennai, Tamil Nadu", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Mumbai University", "city": "Mumbai, Maharashtra", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Calcutta University", "city": "Kolkata, West Bengal", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Panjab University", "city": "Chandigarh", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Lucknow University", "city": "Lucknow, UP", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Allahabad University", "city": "Prayagraj, UP", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Patna University", "city": "Patna, Bihar", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Gauhati University", "city": "Guwahati, Assam", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Jammu University", "city": "Jammu, J&K", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Kashmir University", "city": "Srinagar, J&K", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Manipur University", "city": "Imphal, Manipur", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Sikkim University", "city": "Gangtok, Sikkim", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Tripura University", "city": "Agartala, Tripura", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Mizoram University", "city": "Aizawl, Mizoram", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Assam University", "city": "Silchar, Assam", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Tezpur University", "city": "Tezpur, Assam", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIM Ahmedabad", "city": "Ahmedabad, Gujarat", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIM Bangalore", "city": "Bangalore, Karnataka", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIM Calcutta", "city": "Kolkata, West Bengal", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIM Lucknow", "city": "Lucknow, UP", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIM Kozhikode", "city": "Kozhikode, Kerala", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIM Indore", "city": "Indore, MP", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIM Shillong", "city": "Shillong, Meghalaya", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIM Rohtak", "city": "Rohtak, Haryana", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIM Ranchi", "city": "Ranchi, Jharkhand", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIM Raipur", "city": "Raipur, Chhattisgarh", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIM Trichy", "city": "Tiruchirappalli, Tamil Nadu", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIM Udaipur", "city": "Udaipur, Rajasthan", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIM Nagpur", "city": "Nagpur, Maharashtra", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIM Jammu", "city": "Jammu, J&K", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIIT Hyderabad", "city": "Hyderabad, Telangana", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "IIIT Delhi", "city": "New Delhi", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IIIT Bangalore", "city": "Bangalore, Karnataka", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IIIT Allahabad", "city": "Prayagraj, UP", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIIT Gwalior", "city": "Gwalior, MP", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "IIIT Lucknow", "city": "Lucknow, UP", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "IIIT Pune", "city": "Pune, Maharashtra", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "IIIT Nagpur", "city": "Nagpur, Maharashtra", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Amrita Vishwa Vidyapeetham", "city": "Coimbatore, Tamil Nadu", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "KL University", "city": "Guntur, Andhra Pradesh", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Gitam University", "city": "Visakhapatnam, AP", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Andhra University", "city": "Visakhapatnam, AP", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "JNTU Hyderabad", "city": "Hyderabad, Telangana", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Bangalore University", "city": "Bangalore, Karnataka", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Visvesvaraya Technological University", "city": "Belagavi, Karnataka", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Kerala University", "city": "Thiruvananthapuram, Kerala", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Calicut University", "city": "Malappuram, Kerala", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Cochin University of Science and Technology", "city": "Kochi, Kerala", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "APJ Abdul Kalam Technological University", "city": "Thiruvananthapuram, Kerala", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Savitribai Phule Pune University", "city": "Pune, Maharashtra", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Shivaji University", "city": "Kolhapur, Maharashtra", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Nagpur University", "city": "Nagpur, Maharashtra", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Devi Ahilya Vishwavidyalaya", "city": "Indore, MP", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Barkatullah University", "city": "Bhopal, MP", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Jiwaji University", "city": "Gwalior, MP", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Mohanlal Sukhadia University", "city": "Udaipur, Rajasthan", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Rajasthan University", "city": "Jaipur, Rajasthan", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Guru Nanak Dev University", "city": "Amritsar, Punjab", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "Punjabi University Patiala", "city": "Patiala, Punjab", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "MDU Rohtak", "city": "Rohtak, Haryana", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Kurukshetra University", "city": "Kurukshetra, Haryana", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "AKTU Lucknow", "city": "Lucknow, UP", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Ranchi University", "city": "Ranchi, Jharkhand", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Utkal University", "city": "Bhubaneswar, Odisha", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "Goa University", "city": "Goa", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "Pondicherry University", "city": "Puducherry", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "IGNOU", "city": "New Delhi", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Jamia Millia Islamia", "city": "New Delhi", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "IP University Delhi", "city": "New Delhi", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Sharda University", "city": "Greater Noida, UP", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
    {"name": "GLA University", "city": "Mathura, UP", "image": "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?w=800"},
    {"name": "BIT Mesra", "city": "Ranchi, Jharkhand", "image": "https://images.unsplash.com/photo-1607237138185-eedd9c632b0b?w=800"},
    {"name": "SASTRA University", "city": "Thanjavur, Tamil Nadu", "image": "https://images.unsplash.com/photo-1571260899304-425eee4c7efc?w=800"},
    {"name": "Bharathidasan University", "city": "Tiruchirappalli, Tamil Nadu", "image": "https://images.unsplash.com/photo-1564981797816-1043664bf78d?w=800"},
    {"name": "Bharathiar University", "city": "Coimbatore, Tamil Nadu", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Alagappa University", "city": "Karaikudi, Tamil Nadu", "image": "https://images.unsplash.com/photo-1562774053-701939374585?w=800"},
    {"name": "Annamalai University", "city": "Chidambaram, Tamil Nadu", "image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=800"},
]

# REAL UNIVERSITY IMAGE RESOLVER
# Uses Wikipedia/Wikimedia thumbnails first. If no real image is found,
# it shows a unique name placeholder instead of duplicate stock images.

image_cache = {}

UNIVERSITY_IMAGE_ALIASES = {
    "IIT Delhi": "Indian Institute of Technology Delhi",
    "IIT Bombay": "Indian Institute of Technology Bombay",
    "IIT Madras": "Indian Institute of Technology Madras",
    "IIT Kanpur": "Indian Institute of Technology Kanpur",
    "IIT Kharagpur": "Indian Institute of Technology Kharagpur",
    "IIT Roorkee": "Indian Institute of Technology Roorkee",
    "IIT Guwahati": "Indian Institute of Technology Guwahati",
    "IIT Hyderabad": "Indian Institute of Technology Hyderabad",
    "IIT Bhubaneswar": "Indian Institute of Technology Bhubaneswar",
    "IIT Gandhinagar": "Indian Institute of Technology Gandhinagar",
    "IIT Jodhpur": "Indian Institute of Technology Jodhpur",
    "IIT Mandi": "Indian Institute of Technology Mandi",
    "IIT Patna": "Indian Institute of Technology Patna",
    "IIT Ropar": "Indian Institute of Technology Ropar",
    "IIT Tirupati": "Indian Institute of Technology Tirupati",
    "IIT Palakkad": "Indian Institute of Technology Palakkad",
    "IIT Dharwad": "Indian Institute of Technology Dharwad",
    "IIT Jammu": "Indian Institute of Technology Jammu",
    "IIT Bhilai": "Indian Institute of Technology Bhilai",
    "NIT Trichy": "National Institute of Technology Tiruchirappalli",
    "NIT Warangal": "National Institute of Technology Warangal",
    "NIT Surathkal": "National Institute of Technology Karnataka Surathkal",
    "NIT Calicut": "National Institute of Technology Calicut",
    "NIT Rourkela": "National Institute of Technology Rourkela",
    "NIT Allahabad": "Motilal Nehru National Institute of Technology Allahabad",
    "NIT Jaipur": "Malaviya National Institute of Technology Jaipur",
    "NIT Kurukshetra": "National Institute of Technology Kurukshetra",
    "NIT Durgapur": "National Institute of Technology Durgapur",
    "NIT Surat": "Sardar Vallabhbhai National Institute of Technology Surat",
    "BITS Pilani": "Birla Institute of Technology and Science Pilani",
    "BITS Goa": "BITS Pilani Goa Campus",
    "BITS Hyderabad": "BITS Pilani Hyderabad Campus",
    "VIT Vellore": "Vellore Institute of Technology",
    "VIT Chennai": "VIT Chennai",
    "VIT Bhopal": "VIT Bhopal University",
    "VIT AP": "VIT-AP University",
    "Delhi University": "University of Delhi",
    "Hyderabad University": "University of Hyderabad",
    "Mumbai University": "University of Mumbai",
    "Calcutta University": "University of Calcutta",
    "Panjab University": "Panjab University Chandigarh",
    "Lucknow University": "University of Lucknow",
    "Allahabad University": "University of Allahabad",
    "Patna University": "Patna University",
    "Gauhati University": "Gauhati University",
    "Jammu University": "University of Jammu",
    "Kashmir University": "University of Kashmir",
    "Banaras Hindu University": "Banaras Hindu University",
    "Jawaharlal Nehru University": "Jawaharlal Nehru University",
    "Aligarh Muslim University": "Aligarh Muslim University",
    "Jamia Millia Islamia": "Jamia Millia Islamia",
    "Savitribai Phule Pune University": "Savitribai Phule Pune University",
    "IGNOU": "Indira Gandhi National Open University",
    "IP University Delhi": "Guru Gobind Singh Indraprastha University",
    "AKTU Lucknow": "Dr. A.P.J. Abdul Kalam Technical University",
}


def _fetch_json(url):
    req = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "MessReview/1.0 (https://mess-review-mvp.onrender.com)"
        }
    )
    with urlopen(req, timeout=4) as response:
        return json.loads(response.read().decode("utf-8"))


def _wikipedia_search_thumbnail(query):
    api = "https://en.wikipedia.org/w/api.php"
    search = quote_plus(query)
    url = (
        f"{api}?action=query&format=json&generator=search"
        f"&gsrsearch={search}"
        f"&gsrlimit=5"
        f"&prop=pageimages"
        f"&piprop=thumbnail"
        f"&pithumbsize=1000"
        f"&redirects=1"
    )

    try:
        payload = _fetch_json(url)
        pages = payload.get("query", {}).get("pages", {})
        for page in pages.values():
            thumbnail = page.get("thumbnail", {})
            source = thumbnail.get("source")
            if source:
                return source
    except (URLError, HTTPError, TimeoutError, ValueError):
        return None

    return None


def resolve_university_image(uni, index=1):
    name = uni["name"]
    city = uni["city"]

    if name in image_cache:
        return image_cache[name]

    official_name = UNIVERSITY_IMAGE_ALIASES.get(name, name)
    search_queries = [
        official_name,
        f"{official_name} campus",
        f"{official_name} {city}",
        f"{name} campus India",
        f"{name} university India",
    ]

    for query in search_queries:
        image = _wikipedia_search_thumbnail(query)
        if image:
            image_cache[name] = image
            return image

    fallback = f"https://placehold.co/1200x800/B03A2E/FFFFFF?text={quote_plus(name)}"
    image_cache[name] = fallback
    return fallback


def ensure_real_images(unis):
    for i, uni in enumerate(unis, start=1):
        uni["image"] = resolve_university_image(uni, i)


# HOME PAGE

@app.route("/")
def home():
    conn = get_db_connection()
    reviews = conn.execute("SELECT * FROM reviews ORDER BY id DESC").fetchall()
    ensure_real_images(universities)

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
    if uni:
        ensure_real_images([uni])
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
    ensure_real_images(paginated)

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
            image = f"https://source.unsplash.com/1200x800/?{quote_plus(name + ' ' + city + ' university campus')}"
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
    for i, r in enumerate(results, start=1):
        uni_obj = {"name": r["name"], "city": r["city"]}
        r["image"] = resolve_university_image(uni_obj, i)
    return jsonify(results)

# RUN

if __name__ == "__main__":
    app.run(debug=True)