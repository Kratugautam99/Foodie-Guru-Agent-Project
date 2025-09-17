import sqlite3,os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../data/FoodData.db")
"""This script connects to the SQLite database and retrieves all records from the 'fastfood' table."""
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT * FROM fastfood")
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
col_widths = [20] * len(columns)
header = " | ".join(f"{col:<{w}}" for col, w in zip(columns, col_widths))
print(header)
print("-" * len(header))
for row in rows:
    line = " | ".join(f"{str(val):<{w}}" for val, w in zip(row, col_widths))
    print(line)
conn.close()
