# University Mess Review MVP

A simple website where students can review their university mess food. Built with Python Flask, HTML, CSS, and SQLite.

## Features

- Enter university name
- Rate food from 1 to 5
- Write feedback/review
- Save reviews in SQLite database
- View all reviews on the homepage

## Project Structure

```
mess-review-mvp/
├── app.py              # Flask app and database logic
├── requirements.txt    # Python dependencies
├── reviews.db          # SQLite database (created on first run)
├── templates/
│   └── index.html      # Homepage (form + reviews list)
├── static/
│   └── style.css       # Simple styling
└── README.md           # This file
```

## Requirements

- Python 3.8 or newer
- pip (Python package manager)

## How to Run

### 1. Open terminal in project folder

```bash
cd /Users/macair/Desktop/mess-review-mvp
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Flask app

```bash
python app.py
```

### 5. Open in browser

Visit: **http://127.0.0.1:5000**

## Usage

1. Fill in your university name.
2. Select a food rating (1 to 5).
3. Write your feedback.
4. Click **Submit Review**.
5. Your review appears in the **All Reviews** section below.

## Notes

- The SQLite file `reviews.db` is created automatically when you run the app.
- `debug=True` is enabled for learning; turn it off before deploying to production.
