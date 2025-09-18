import pandas as pd
import sqlite3, os, json
from datetime import datetime
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db_path = os.path.join(PROJECT_ROOT, "data", "Analytics.db")
db_path = os.path.abspath(db_path)

# Initialize the database and create the conversations table if it doesn't exist
def init_db():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        user_message TEXT,
        bot_reply TEXT,
        interest_score INTEGER,
        filters TEXT,
        products TEXT,
        timestamp DATETIME
    )
    """)
    conn.commit()
    conn.close()

# Log a conversation entry
def log_conversation(session_id, user_message, bot_reply, interest_score, filters, products):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    init_db()
    cur.execute("""
        INSERT INTO conversations (session_id, user_message, bot_reply, interest_score, filters, products, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        session_id,
        user_message,
        bot_reply,
        interest_score,
        json.dumps(filters),
        json.dumps(products),
        datetime.now()
    ))
    conn.commit()
    conn.close()

# Analytics functions
def get_interest_progression(session_id):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(
        "SELECT timestamp, interest_score FROM conversations WHERE session_id=? ORDER BY timestamp",
        conn, params=(session_id,)
    )
    conn.close()
    return df

# Average duration of conversations
def get_average_duration():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT session_id, MIN(timestamp) as start, MAX(timestamp) as end FROM conversations GROUP BY session_id", conn)
    df["duration"] = pd.to_datetime(df["end"]) - pd.to_datetime(df["start"])
    return df["duration"].mean()

# Most recommended products
def get_most_recommended_products():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT products FROM conversations", conn)
    conn.close()
    all_products = []
    for row in df["products"]:
        try:
            all_products.extend([p["name"] for p in json.loads(row)])
        except:
            pass
    return pd.Series(all_products).value_counts()

# Drop-off points (sessions with low interest_score)
def get_drop_off_points():
    """
    Returns session IDs where interest_score is 0 (drop-offs).
    db_path: path to SQL database file
    session_id: optional, filter for a specific session
    """
    conn = sqlite3.connect(db_path)
    query = "SELECT session_id FROM conversations WHERE interest_score < 20"
    df = pd.read_sql(query, conn)
    
    conn.close()
    return df['session_id'].unique().tolist()

# Highest converting products (products from sessions with high interest_score)
def get_highest_converting_products():
    """
    Returns products sorted by total interest_score.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT products, interest_score FROM conversations", conn)
    conn.close()
    
    import ast
    product_scores = {}
    
    for _, row in df.iterrows():
        products = ast.literal_eval(row['products'])
        score = row['interest_score']
        for product in products:
            pid = product['product_id']
            product_scores[pid] = product_scores.get(pid, 0) + score
    
    sorted_products = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_products

# Get the last interest score for a session
def get_last_interest_score(session_id: str) -> int:
    conn = sqlite3.connect(db_path)
    row = conn.execute(
        """
        SELECT interest_score
        FROM conversations
        WHERE session_id=?
        ORDER BY timestamp DESC
        LIMIT 1
        """,
        (session_id,)
    ).fetchone()
    conn.close()
    return row[0] if row else 0