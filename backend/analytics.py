import pandas as pd
import sqlite3, os, json, ast, re
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
    df = pd.read_sql_query("""
        SELECT 
            session_id, 
            DATE(timestamp) as day, 
            MIN(timestamp) as start, 
            MAX(timestamp) as end
        FROM conversations
        GROUP BY session_id, day
    """, conn)
    conn.close()
    df["duration"] = pd.to_datetime(df["end"]) - pd.to_datetime(df["start"])
    avg_per_day = df.groupby("day")["duration"].mean()
    result = {
        day: f"{int(val.total_seconds()//3600)}h {int((val.total_seconds()%3600)//60)}m"
        for day, val in avg_per_day.items()
    }
    return result

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

# Drop-off points (based on product ids)
def get_drop_off_points():
    """
    Returns the last five drop-off points with both product_id and product name.
    Drop-off = products shown but interest_score == 0.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(
        "SELECT rowid, timestamp, interest_score, products FROM conversations ORDER BY timestamp DESC",
        conn
    )
    conn.close()
    drop_off_products = []
    for _, row in df.iterrows():
        products = []
        if row["products"]:
            try:
                products = ast.literal_eval(row["products"])
            except Exception:
                try:
                    products = json.loads(row["products"])
                except Exception:
                    products = []
        if products and row["interest_score"] == 0:
            for product in products:
                drop_off_products.append((product["product_id"], product["name"]))
    return drop_off_products[:5]

# Highest converting products (products from sessions with high interest_score)
def get_highest_converting_products():
    """
    Returns products sorted by total interest_score.
    Automatically maps 'pack up ...' queries back to product_id and product_name.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(
        "SELECT session_id, user_message, products, interest_score FROM conversations",
        conn
    )
    conn.close()
    product_scores = {}
    session_products = {}
    for _, row in df.iterrows():
        session_id = row["session_id"]
        query = row["user_message"].lower()
        score = row["interest_score"]
        products = []
        if row["products"]:
            try:
                products = ast.literal_eval(row["products"])
            except Exception:
                try:
                    products = json.loads(row["products"])
                except Exception:
                    products = []
        if products:
            if session_id not in session_products:
                session_products[session_id] = []
            session_products[session_id].extend(products)
        if "pack up" in query:
            match = re.search(r"pack up (.+)", query)
            if match:
                ordered_name = match.group(1).strip().lower()
                for product in session_products.get(session_id, []):
                    if ordered_name in product["name"].lower():
                        pid = product["product_id"]
                        pname = product["name"]
                        key = (pid, pname)
                        product_scores[key] = product_scores.get(key, 0) + score
                        break
    sorted_products = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)
    return [(pid, pname, min(score, 100)) for (pid, pname), score in sorted_products]


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