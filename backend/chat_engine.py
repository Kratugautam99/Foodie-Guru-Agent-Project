import os
import json
from dotenv import load_dotenv
from groq import Groq
from .filter_functions import get_fastfood_by_filters, get_unique_values
from .analytics import log_conversation, get_last_interest_score


# Initialize the Groq client using the API key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
conversation_memory = {}
# Main function to analyze user message and generate response
def analyze_message(user_message: str, session_id: str):
    interest_score = get_last_interest_score(session_id)
    """
    Analyze user's message, maintain memory of last 3 messages,
    extract filters, calculate interest score, fetch fastfoods, 
    and generate a friendly response.
    """
    
    results = get_unique_values()
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []
    conversation_memory[session_id].append({"role": "user", "content": user_message})
    conversation_memory[session_id] = conversation_memory[session_id][-3:]

    system_prompt = f"""
    Your Name is FoodieGuru, an enthusiastic and helpful AI assistant for a fast food restaurant and suggest people dishes according to their cravings
    After user says that he/she wants to order you should reply with order will arrive in 30 mins.
    Your goal is to understand the customer's cravings, dietary needs, budget, and mood to recommend the perfect meal from the menu.
    Always be polite, engaging, and excited about the food. boolean values should be True/False. 
    

    Last interest score = {interest_score}.
    Rules:
    - if Last interest score is already 100, then set to 0.
    - Add +15 if user expresses specific preference (e.g. craving, delighted, favorite).
    - Add +20 if user shows mood/emotion (happy, sad, hungry, excited).
    - Add +10 if user asks a question.
    - Add +25 if user uses enthusiasm words (amazing, delicious, awesome, thrilled).
    - Add +25 if user mentions price or budget.
    - Subtract -10 for hesitation (maybe).
    - Subtract -15 for budget concern (too expensive).
    - Subtract -20 for dietary conflict (allergic).
    - Subtract -25 for rejection (no).
    - Subtract -5 for delay (later).
    - If user says "pack up" or "i will order" → set score to 100.
    - Max score is 100, Min is -100

    **CRITICAL INSTRUCTIONS:**
    - Analyze the user's input and extract the following parameters for a database query:
    * category (options=>, {', '.join(results['categories'])}) -> cant be empty, use only options
    * max_price (numeric value if user mentions budget)
    * mood_tags (e.g., {', '.join(results['mood_tags'])})
    * dietary_tags (e.g., {', '.join(results['dietary_tags'])})
    * allergens_exclude (e.g., {', '.join(results['allergens'])})
    * chef_special (boolean if user wants special items)
    * min_popularity (minimum numeric value threshold if user mentions popular or best-selling items)
    * ingredients_include (e.g., {', '.join(results['ingredients'])})
    * max_calories (numeric value if user mentions calorie limit → interpret as max calories)
    * limited_time (boolean if user wants limited-time offers)
    * min_spice (numeric if user requests spiciness, e.g. 5+)
    * max_spice (numeric if user requests mildness, e.g. up to 3)
    * interest_score (calculated according to the rules above)
    * count (number of items to return, default to 3 if not specified)
    * debug (boolean, set to True if user wants to see SQL query)

    - Your response must be a JSON object with this exact structure from below example:
    {{
    "reply": "Your friendly response here...",
    "filters": {{
        "category": "Burgers",
        "max_price": 10.0,
        "mood_tags": ["adventurous", "comfort"],
        "dietary_tags": ["spicy"],
        "allergens_exclude": ["soy"],
        "chef_special": False,
        "min_popularity": 45,
        "ingredients_include": ["beef patty"],
        "max_calories": 700,
        "limited_time": True,
        "min_spice": 3,
        "max_spice": 8,
        "interest_score": 45
        "count" : 3
        "debug" : False
    }}
    }}
    """

    messages = [{"role": "system", "content": system_prompt}] + conversation_memory[session_id]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="qwen/qwen3-32b",
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
        ingredients_include=extracted_filters.get("ingredients_include"),
        calories=extracted_filters.get("max_calories"),
        popularity=extracted_filters.get("min_popularity"),
        count=extracted_filters.get("count", 3),
        debug=extracted_filters.get("debug", False)
    )   

    suggested_fastfoods = [dict(item) for item in suggested_fastfoods]

    interest_score = extracted_filters.get("interest_score", 30)
    bot_reply = llm_response["reply"]

    log_conversation(
        session_id=session_id,
        user_message=user_message,
        bot_reply=bot_reply,
        interest_score=interest_score,
        filters=extracted_filters,
        products=[dict(item) for item in suggested_fastfoods]
    )

    if suggested_fastfoods:
        top_product = suggested_fastfoods[0]
        bot_reply += f" How about our '{top_product['name']}' for ${top_product['price']}?"

    return {
        "reply": bot_reply,
        "suggested_fastfoods": suggested_fastfoods,
        "interest_score": interest_score,
        "session_id": session_id
    }
