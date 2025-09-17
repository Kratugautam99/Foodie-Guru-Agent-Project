import os
import json
from dotenv import load_dotenv
from groq import Groq
from .filter_functions import get_fastfood_by_filters, get_unique_values

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client using the API key from .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_message(user_message: str, session_id: str):
    """
    1. Analyzes the user's message using Groq.
    2. Extracts filters for database query.
    3. Calculates interest score.
    4. Fetches fastfoods from DB.
    5. Generates a friendly response.
    """
    
    results = get_unique_values()

    system_prompt = f"""
    You are FoodieBot, an enthusiastic and helpful AI assistant for a fast food restaurant.
    Your goal is to understand the customer's cravings, dietary needs, budget, and mood to recommend the perfect meal from the menu.
    Always be polite, engaging, and excited about the food. boolean values should be True/False.
    
    ENGAGEMENT_FACTORS = [
        'specific_preferences': +15,    # e.g., I love spicy Korean food
        'dietary_restrictions': +10,    # e.g., I am vegetarian
        'budget_mention': +5,           # e.g., Under $15
        'mood_indication': +20,         # e.g., I am feeling adventurous
        'question_asking': +10,         # e.g., What is the spice level?
        'enthusiasm_words': +8,         # e.g., amazing, perfect, love
        'price_inquiry': +25,           # e.g., How much is that?
        'order_intent': +30             # e.g., I will take it, Add to cart
    ]

    NEGATIVE_FACTORS = [
        'hesitation': -10,              # e.g., maybe, not sure
        'budget_concern': -15,          # e.g., too expensive
        'dietary_conflict': -20,        # e.g., Product doesn't match restrictions
        'rejection': -25,               # e.g., I don't like that
        'delay_response': -5            # e.g., Long response time
    ]
    calculate an interest score based on these factors to gauge how interested the user is in ordering use above format.

    **CRITICAL INSTRUCTIONS:**
    - Analyze the user's input and extract the following parameters for a database query:
    * category (e.g., {', '.join(results['categories'])}) this category should have 1st alphabet capitalized unlike other categorical categories.
    * max_price (numeric value if user mentions budget)
    * mood_tags (e.g., {', '.join(results['mood_tags'])})
    * dietary_tags (e.g., {', '.join(results['dietary_tags'])})
    * allergens_exclude (e.g., {', '.join(results['allergens'])})
    * chef_special (boolean if user wants special items)
    * popularity (boolean if user mentions popular or best-selling items)
    * ingredients_include (e.g., {', '.join(results['ingredients'])})
    * calories (numeric value if user mentions calorie limit → interpret as max calories)
    * limited_time (boolean if user wants limited-time offers)
    * min_spice (numeric if user requests spiciness, e.g. 5+)
    * max_spice (numeric if user requests mildness, e.g. up to 3)

    - Your response must be a JSON object with this exact structure:
    {{
    "reply": "Your friendly response here...",
    "filters": {{
        "category": "Burgers",
        "max_price": 10.0,
        "mood_tags": ["adventurous"],
        "dietary_tags": ["spicy"],
        "allergens_exclude": ["soy"],
        "chef_special": False,
        "popularity": False,
        "ingredients_include": ["beef patty"],
        "calories": 700,
        "limited_time": True,
        "min_spice": 3,
        "max_spice": 8
        "interest_score": 45
    }}
    }}
    - Calculate the interest_score based on the ENGAGEMENT_FACTORS and NEGATIVE_FACTORS above and include it in the filters. Note interest_score cant be negative or None, and Default value should be 0.
    - If a parameter is not mentioned by the user, set its value to None.
    - Only suggest menu items that exist in the database. Do not make up menu items.
    """


    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        model="deepseek-r1-distill-llama-70b",
        temperature=0.7,
        response_format={"type": "json_object"}
    )

    llm_response = json.loads(chat_completion.choices[0].message.content)
    extracted_filters = llm_response.get("filters", {})

    suggested_fastfoods = get_fastfood_by_filters(
    category=extracted_filters.get("category"),
    max_price=extracted_filters.get("max_price"),
    mood_tags=extracted_filters.get("mood_tags"),
    dietary_tags=extracted_filters.get("dietary_tags"),
    allergens_exclude=extracted_filters.get("allergens_exclude"),
    chef_special=extracted_filters.get("chef_special"),
    limited_time=extracted_filters.get("limited_time"),
    min_spice=extracted_filters.get("min_spice"),
    max_spice=extracted_filters.get("max_spice"),
    limit=3,
)   
    suggested_fastfoods = [dict(item) for item in suggested_fastfoods]  # Convert sqlite3.Row to dict

    interest_score = extracted_filters.get("interest_score")

    bot_reply = llm_response["reply"]

    if suggested_fastfoods:
        top_product = suggested_fastfoods[0]
        bot_reply += f" How about our '{top_product['name']}' for ${top_product['price']}?"

    return {
        "reply": bot_reply,
        "suggested_fastfoods": suggested_fastfoods,
        "interest_score": interest_score,
        "session_id": session_id
    }

