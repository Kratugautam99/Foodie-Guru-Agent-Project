from PIL import Image
import streamlit as st
from io import BytesIO
import requests, json, os
from typing import Any, List, Dict
# ----------------------
# Page / Theme Setup
# ----------------------
st.set_page_config(page_title="Foodie-Guru", page_icon="https://raw.githubusercontent.com/Kratugautam99/FoodieBotAgent-Project/refs/heads/main/Images/Icon/icon.png", layout="wide")

# Custom CSS for a nicer look and message backgrounds
PAGE_CSS = """
<style>
/* Page background and fonts */
body, .stApp {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.stApp {
  background: linear-gradient(180deg, rgba(10,10,10,0.6), rgba(30,30,30,0.6)), url('https://raw.githubusercontent.com/Kratugautam99/FoodieBotAgent-Project/refs/heads/main/Images/background/bg.jpg');
  background-size: cover;
  background-attachment: fixed;
  color: #fff;
}

/* Header area */
.header-card {
  background: rgba(0,0,0,0.45);
  padding: 12px 18px;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.45);
}

/* Chat bubbles */
.user-bubble, .assistant-bubble {
  padding: 14px 18px;
  margin: 6px 0;
  border-radius: 14px;
  max-width: 78%;
  line-height: 1.4;
}
.user-bubble {
  background: linear-gradient(90deg,#0f172a, #0b1220);
  border: 1px solid rgba(255,255,255,0.04);
  color: #d1d5db;
  margin-left: auto;
}
.assistant-bubble {
  background-image: url('https://raw.githubusercontent.com/Kratugautam99/FoodieBotAgent-Project/refs/heads/main/Images/background/bot.gif');
  background-size: cover;
  background-position: center;
  color: #fff;
  border: 1px solid rgba(255,255,255,0.06);
  box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}
.assistant-bubble h3 { margin: 0 0 8px 0; }

/* Product card style inside expanders */
.product-card {
  background: rgba(255,255,255,0.03);
  padding: 10px;
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.03);
}

/* Sidebar tweaks */
.stSidebar { background: rgba(0,0,0,0.5); }

/* Make metrics stand out */
.metric-value { color: #fff !important; }

@media (max-width: 640px) {
  .user-bubble, .assistant-bubble { max-width: 94%; }
}
</style>
"""
st.markdown(PAGE_CSS, unsafe_allow_html=True)

# Top layout with logo + title
col1, col2 = st.columns([1, 4])
with col1:
    # Use emoji if local image not available
    try:
        st.image("https://raw.githubusercontent.com/Kratugautam99/FoodieBotAgent-Project/refs/heads/main/Images/Icon/icon.png", width=180)
    except Exception:
        st.markdown("<div style='font-size:48px'>https://raw.githubusercontent.com/Kratugautam99/FoodieBotAgent-Project/refs/heads/main/Images/Icon/icon.png</div>", unsafe_allow_html=True)
with col2:
    st.markdown('''<div class="header-card">
<h1 style="color: #5eead4; margin:0">Foodie-Guru</h1>
<p style="margin:0; color:#c7f9f1;">Your friendly fast-food concierge — tell me what you crave.</p>
</div>''', unsafe_allow_html=True)

# Default backend URL (matches backend main.py)
DEFAULT_API_URL = os.environ.get("FOODIEBOT_API_URL", "http://localhost:8000/chat")

# Initialize session state
if "messages" not in st.session_state:
    messages: List[Dict[str, Any]] = []
    st.session_state.messages = messages
if "session_id" not in st.session_state:
    st.session_state.session_id = "default_session"
if "api_url" not in st.session_state:
    st.session_state.api_url = DEFAULT_API_URL


# ----------------------
# Helper functions
# ----------------------

def safe_json_loads(value: Any) -> Any:
    """Try to parse a JSON string into Python object; otherwise return original or split comma string."""
    if value is None:
        return None
    if isinstance(value, (list, dict)):
        return value
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return None
        try:
            parsed = json.loads(value)
            return parsed
        except Exception:
            # fallback: comma-separated tokens
            if "," in value:
                return [t.strip() for t in value.split(",") if t.strip()]
            return value
    return value


def display_tags(tags: Any, tag_type: str = "default") -> str:
    """Return a small emoji-prefixed string for tags (works with list or json string)."""
    parsed = safe_json_loads(tags)
    if not parsed:
        return ""
    if isinstance(parsed, str):
        return f"🏷️ {parsed}"
    if isinstance(parsed, list):
        tag_colors = {
            "mood": "🔹",
            "dietary": "✅",
            "allergen": "⚠️",
            "default": "🏷️",
        }
        emoji = tag_colors.get(tag_type, "🏷️")
        return f"{emoji} " + " • ".join(str(x) for x in parsed)
    # fallback
    return str(parsed)


def normalize_product(product: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure product dict fields are in expected python types for display."""
    p = dict(product)  # shallow copy
    # Parse fields that might be stored as JSON strings
    for key in ["mood_tags", "dietary_tags", "allergens", "ingredients"]:
        if key in p:
            p[key] = safe_json_loads(p[key])
    # Numeric fallbacks
    p["price"] = p.get("price") or 0.0
    p["calories"] = p.get("calories") or "N/A"
    p["spice_level"] = p.get("spice_level") or "N/A"
    p["popularity_score"] = p.get("popularity_score") or "N/A"
    p["chef_special"] = bool(p.get("chef_special"))
    p["limited_time"] = bool(p.get("limited_time"))
    # Preserve image_prompt field
    p["image_prompt"] = p.get("image_prompt")
    return p

def generate_image_from_prompt(product: dict) -> str:
    id = int(product.get("product_id")[2:])
    url = f"https://raw.githubusercontent.com/Kratugautam99/FoodieBotAgent-Project/main/Images/database_images/{id}.jpg"
    return url

# ----------------------
# Sidebar controls
# ----------------------
with st.sidebar:
    st.header("⚙️ Settings")
    api_input = st.text_input("Backend API URL", value=st.session_state.api_url)
    if api_input and api_input != st.session_state.api_url:
        st.session_state.api_url = api_input
    st.write("")
    st.write("If your backend is running on a different host/port, update the URL above.")
    st.write("")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.session_id = f"session_{hash(str(st.session_state))}"
        st.experimental_rerun()


# ----------------------
# Render chat history
# ----------------------
for message in st.session_state.messages:
    role = message.get("role", "assistant")
    content = message.get("content", "")
    with st.chat_message(role):
        # Allow HTML so our bubbles render with background images / gradients
        st.markdown(content, unsafe_allow_html=True)

        fastfoods = message.get("fastfoods") or message.get("products") or []
        if fastfoods:
            # Show product cards in a responsive two-column grid
            cols = st.columns(2)
            for idx, raw_product in enumerate(fastfoods):
                product = normalize_product(raw_product)
                with cols[idx % 2]:
                    with st.expander(f"🍔 {product.get('name')} - ${product.get('price')}", expanded=True):
                        st.markdown(f"<div class='product-card'>", unsafe_allow_html=True)

                        # Render image if image_prompt exists (supports URL, local file, or prompt -> Unsplash)
                        image_url = generate_image_from_prompt(product) 
                        if image_url:
                            try:
                                response = requests.get(image_url)
                                img = Image.open(BytesIO(response.content))
                                img = img.resize((500, 300))
                                # Streamlit will accept both remote URLs and local file paths
                                st.image(img, caption=f"Image: {product.get('image_prompt')}")
                            except Exception as e:
                                st.text(f"Error: {e}")

                        st.write(f"**Description:** {product.get('description')}")
                        st.write(f"**Category:** {product.get('category')}")

                        # Nutritional info
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Calories", product.get('calories'))
                        with col2:
                            st.metric("Spice Level", f"{product.get('spice_level')}/10" if isinstance(product.get('spice_level'), int) else product.get('spice_level'))
                        with col3:
                            st.metric("Popularity", f"{product.get('popularity_score')}%" if isinstance(product.get('popularity_score'), int) else product.get('popularity_score'))

                        st.write(f"**Prep Time:** {product.get('prep_time')}")

                        if product.get('mood_tags'):
                            st.write(display_tags(product.get('mood_tags'), "mood"))
                        if product.get('dietary_tags'):
                            st.write(display_tags(product.get('dietary_tags'), "dietary"))

                        if product.get('allergens'):
                            allergens = product.get('allergens')
                            if isinstance(allergens, list):
                                st.warning(f"**Contains:** {', '.join(allergens)}")
                            else:
                                st.warning(f"**Contains:** {allergens}")

                        badge_col = st.columns(2)
                        with badge_col[0]:
                            if product.get('chef_special'):
                                st.success("👨‍🍳 Chef's Special")
                        with badge_col[1]:
                            if product.get('limited_time'):
                                st.error("⏰ Limited Time")
                        st.markdown(f"</div>", unsafe_allow_html=True)



# ----------------------
# Chat input and send
# ----------------------
if prompt := st.chat_input("What are you craving today?"):
    # Wrap user message in styled bubble and append to history
    user_html = f"<div class='user-bubble'>{prompt}</div>"
    st.session_state.messages.append({"role": "user", "content": user_html})
    with st.chat_message("user"):
        st.markdown(user_html, unsafe_allow_html=True)

    # Prepare payload
    payload = {
        "message": prompt,
        "session_id": st.session_state.session_id,
    }

    # Send to backend
    with st.chat_message("assistant"):
        with st.spinner("FoodieBot is thinking..."):
            try:
                response = requests.post(st.session_state.api_url, json=payload, timeout=12)
                # Raise for non-2xx
                response.raise_for_status()
                response_data = response.json()

                bot_reply = response_data.get("reply", "")
                interest_score = response_data.get("interest_score", 0)
                suggested_fastfoods = response_data.get("suggested_fastfoods") or []

                # Wrap assistant reply in a beautiful background bubble
                assistant_html = f"""<div class='assistant-bubble'>
                                    <h3>Foodie-Guru</h3>
                                    <p>{bot_reply}</p>
                                    </div>"""

                # Display wrapped reply
                st.markdown(assistant_html, unsafe_allow_html=True)

                # Show interest score as a metric (0-100)
                st.metric(label="Interest Score", value=f"{interest_score}%", delta_color="off")

                # Display suggested fastfoods
                if suggested_fastfoods:
                    st.subheader("🍽️ Suggestions for you:")
                    cols = st.columns(2)
                    for idx, raw_product in enumerate(suggested_fastfoods):
                        product = normalize_product(raw_product)
                        with cols[idx % 2]:
                            with st.expander(f"🍔 {product.get('name')} - ${product.get('price')}", expanded=True):
                                st.markdown(f"<div class='product-card'>", unsafe_allow_html=True)

                                image_url = generate_image_from_prompt(product) 
                                if image_url:
                                    try:
                                        response = requests.get(image_url)
                                        img = Image.open(BytesIO(response.content))
                                        img = img.resize((500, 300))
                                        # Streamlit will accept both remote URLs and local file paths
                                        st.image(img, caption=f"Image: {product.get('image_prompt')}")
                                    except Exception as e:
                                        st.text(f"Error: {e}")

                                st.write(f"**Description:** {product.get('description')}")
                                st.write(f"**Category:** {product.get('category')}")

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Calories", product.get('calories'))
                                with col2:
                                    st.metric("Spice Level", f"{product.get('spice_level')}/10" if isinstance(product.get('spice_level'), int) else product.get('spice_level'))
                                with col3:
                                    st.metric("Popularity", f"{product.get('popularity_score')}%" if isinstance(product.get('popularity_score'), int) else product.get('popularity_score'))

                                st.write(f"**Prep Time:** {product.get('prep_time')}")

                                if product.get('mood_tags'):
                                    st.write(display_tags(product.get('mood_tags'), "mood"))
                                if product.get('dietary_tags'):
                                    st.write(display_tags(product.get('dietary_tags'), "dietary"))

                                if product.get('allergens'):
                                    allergens = product.get('allergens')
                                    if isinstance(allergens, list):
                                        st.warning(f"**Contains:** {', '.join(allergens)}")
                                    else:
                                        st.warning(f"**Contains:** {allergens}")

                                badge_col = st.columns(2)
                                with badge_col[0]:
                                    if product.get('chef_special'):
                                        st.success("👨‍🍳 Chef's Special")
                                with badge_col[1]:
                                    if product.get('limited_time'):
                                        st.error("⏰ Limited Time")
                                st.markdown(f"</div>", unsafe_allow_html=True)

                # Save assistant message + fastfoods to session history (store HTML so it keeps styling)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_html,
                    "fastfoods": suggested_fastfoods,
                })

            except requests.exceptions.RequestException as e:
                st.error(f"Sorry, I'm having trouble connecting to the kitchen! (Error: {e})")
            except json.JSONDecodeError as e:
                st.error(f"Error parsing response from server: {e}")


# Footer / about
with st.sidebar:
    st.header("ℹ️ About FoodieBot")
    st.write("I'm your AI food assistant! I can help you find the perfect meal based on:")
    st.write("• Your mood 😊 🎉 😋")
    st.write("• Dietary preferences 🥗 🌱 🌶️")
    st.write("• Budget 💰")
    st.write("• Allergies and restrictions ⚠️")
    st.write("")
    st.write("Backend API: ", st.session_state.api_url)
