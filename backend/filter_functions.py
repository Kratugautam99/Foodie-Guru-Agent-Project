import sqlite3, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../data/FoodData.db")

def get_fastfood_by_filters(
    category=None,
    max_price=None,
    mood_tags=None,
    dietary_tags=None,
    allergens_exclude=None,
    chef_special=None,
    popularity=None,
    ingredients_include=None,
    calories=None,
    limited_time=None,
    min_spice=None,
    max_spice=None,
    limit=5,
    debug=None
):
    """
    Query fastfood from the database based on flexible filters.
    Returns a list of sqlite3.Row (dict-like).
    """
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    
    query = "SELECT * FROM fastfood WHERE 1=1"
    params = []

    # Category
    if category:
        query += " AND category = ?"
        params.append(category)

    # Price
    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)

    # Mood tags
    if mood_tags:
        for tag in mood_tags:
            query += " AND mood_tags LIKE ?"
            params.append(f"%{tag}%")

    # Dietary tags
    if dietary_tags:
        for tag in dietary_tags:
            query += " AND dietary_tags LIKE ?"
            params.append(f"%{tag}%")
    
    # Ingredients (include foods containing certain ingredients)
    if ingredients_include:
        for ingredient in ingredients_include:
            query += " AND ingredients LIKE ?"
            params.append(f"%{ingredient}%")

    # Allergens (exclude foods containing certain allergens)
    if allergens_exclude:
        for allergen in allergens_exclude:
            query += " AND allergens NOT LIKE ?"
            params.append(f"%{allergen}%")

    # Chef special
    if chef_special is not None:
        query += " AND chef_special = ?"
        params.append(1 if chef_special else 0)

    # Limited time
    if limited_time is not None:
        query += " AND limited_time = ?"
        params.append(1 if limited_time else 0)

    # Spice level
    if min_spice is not None:
        query += " AND spice_level >= ?"
        params.append(min_spice)
    if max_spice is not None:
        query += " AND spice_level <= ?"
        params.append(max_spice)

    # Calories
    if calories is not None:
        query += " AND calories <= ?"
        params.append(calories)

    # Order by popularity
    if popularity:
        query += " ORDER BY popularity_score DESC LIMIT ?"
        params.append(limit)
    else:
        query += " LIMIT ?"
        params.append(limit)
    
    
    if debug:
        print("DEBUG SQL:", query)
        print("DEBUG PARAMS:", params)

    cursor = conn.execute(query, params)
    fastfood = cursor.fetchall()
    conn.close()
    return fastfood


def get_unique_values():
    """
    Extract unique values from categorical columns.
    Handles comma-separated/JSON-style arrays as well.
    """
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = lambda cursor, row: row[0]  # return single column
    
    results = {}

    # Category (simple)
    results["categories"] = list(set(conn.execute("SELECT category FROM fastfood").fetchall()))

    # Mood tags
    mood_rows = conn.execute("SELECT mood_tags FROM fastfood").fetchall()
    mood_tags = set()
    for row in mood_rows:
        if row:  # row may be JSON or comma-separated
            for tag in str(row).replace("[","").replace("]","").replace("'","").split(","):
                mood_tags.add(tag.strip())
    results["mood_tags"] = sorted(mood_tags)

    # Dietary tags
    diet_rows = conn.execute("SELECT dietary_tags FROM fastfood").fetchall()
    dietary_tags = set()
    for row in diet_rows:
        if row:
            for tag in str(row).replace("[","").replace("]","").replace("'","").split(","):
                dietary_tags.add(tag.strip())
    results["dietary_tags"] = sorted(dietary_tags)

    # Allergens
    allergen_rows = conn.execute("SELECT allergens FROM fastfood").fetchall()
    allergens = set()
    for row in allergen_rows:
        if row:
            for tag in str(row).replace("[","").replace("]","").replace("'","").split(","):
                allergens.add(tag.strip())
    results["allergens"] = sorted(allergens)

    # Ingredients
    ingredient_rows = conn.execute("SELECT ingredients FROM fastfood").fetchall()
    ingredients = set()
    for row in ingredient_rows:
        if row:
            for tag in str(row).replace("[","").replace("]","").replace("'","").split(","):
                ingredients.add(tag.strip())
    results["ingredients"] = sorted(ingredients)

    conn.close()
    return results
