# Database Writer through SQLite
import sqlite3, json, os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../data/FoodData.db")
db_path = os.path.abspath(db_path)
json_path = os.path.join(BASE_DIR, "../data/FoodData.json")
json_path = os.path.abspath(json_path)
"""Initializes the database and creates the fastfood table if it doesn't exist."""
data = json.load(open(json_path))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS fastfood (
        product_id TEXT PRIMARY KEY,
        name TEXT,
        category TEXT,
        description TEXT,
        ingredients TEXT,
        price REAL,
        calories INTEGER,
        prep_time INTEGER,
        dietary_tags TEXT,
        mood_tags TEXT,
        allergens TEXT,
        popularity_score REAL,
        chef_special INTEGER,
        limited_time INTEGER,
        spice_level INTEGER,
        image_prompt TEXT
    )
""")

for item in data:
    cursor.execute("""
    INSERT INTO fastfood VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    item['product_id'],
    item['name'],
    item['category'],
    item['description'],
    json.dumps(item['ingredients']),
    item['price'],
    item['calories'],
    item['prep_time'],
    json.dumps(item['dietary_tags']),
    json.dumps(item['mood_tags']),
    json.dumps(item['allergens']),
    item['popularity_score'],
    int(item['chef_special']),
    int(item['limited_time']),
    item['spice_level'],
    item['image_prompt']
))

conn.commit()
conn.close()