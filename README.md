<p align="center">
  <img src="https://raw.githubusercontent.com/Kratugautam99/Foodie-Guru-Agent-Project/refs/heads/main/Images/Icon/icon.png" alt="FoodieGuruAgent Logo" width="400" />
  <h1 align="center">Foodie-Guru-Agent</h1>
  <p align="center">
    🍔 Your AI-powered culinary companion — delivering smart, mood‑aware, and personalized fast‑food recommendations in real time 🚀
  </p>
</p>

---

**Foodie-Guru-Agent** isn’t just another chatbot — it’s a full‑stack, agent‑driven food discovery experience.  
It listens like a friend, thinks like a data scientist, and recommends like a seasoned foodie.  
Powered by a **FastAPI** backend and a sleek **Streamlit** frontend, it taps into a curated **SQLite** database of 100 AI‑generated menu items to serve you the perfect bite, every time.

Whether you’re craving a midnight burger, looking for vegan pizza, or just curious about what fits your budget and mood, FoodieGuruAgent blends **natural conversation**, **real‑time analytics**, and **smart filtering** to make every recommendation feel tailor‑made.  
From mood detection to interest scoring, from database queries to live dashboards — it’s your personal food concierge, available 24/7.

---


## 🚀 Live Demo

- Frontend Chat Interface (Streamlit):  
  https://kratugautam-foodieguruagent-project.streamlit.app

- Backend API (FastAPI) [Not-Deployed-Standalonely]:  
  http://localhost:8000

---

## 🖼️ Demo Screenshots

<p align="center">
  <img src="https://raw.githubusercontent.com/Kratugautam99/Foodie-Guru-Agent-Project/refs/heads/main/Images/demo/1.png" alt="FoodieBot Demo 1" width="45%" />
  <img src="https://raw.githubusercontent.com/Kratugautam99/Foodie-Guru-Agent-Project/refs/heads/main/Images/demo/2.png" alt="FoodieBot Demo 2" width="45%" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Kratugautam99/Foodie-Guru-Agent-Project/refs/heads/main/Images/demo/3.png" alt="FoodieBot Demo 3" width="45%" />
  <img src="https://raw.githubusercontent.com/Kratugautam99/Foodie-Guru-Agent-Project/refs/heads/main/Images/demo/4.png" alt="FoodieBot Demo 4" width="45%" />
</p>

<p align="center">
  <em>Interactive chat, personalized recommendations, and real-time analytics — all in action!</em>
</p>

---

## ✨ Key Features

- **Natural Dialogue**  
  Understands user intent, moods, dietary needs, and price constraints.

- **Dynamic Interest Scoring**  
  Calculates a real-time “interest score” (0–100%) based on engagement signals (enthusiasm, order intent, budget mentions, etc.).

- **Smart Product Recommendations**  
  Filters and ranks items by mood tags, dietary tags, price range, popularity score, and real-time availability.

- **Database-Driven Responses**  
  Queries a SQLite database of 100 AI-generated fast-food products across 10 categories (Burgers, Pizza, Tacos, Desserts, and more).

- **Analytics Dashboard**  
  Tracks conversation metrics (interest score progression, drop-off points) and product performance (conversion rates, category analysis).

- **Full-Stack Python**  
  Backend with FastAPI; frontend with Streamlit; data persistence in SQLite.

---

## 🛠 Tech Stack

| Component               | Technology                |
|-------------------------|---------------------------|
| Backend Framework       | FastAPI                   |
| Frontend Framework      | Streamlit                 |
| Database                | SQLite (FoodData.db, Analytics.db) |
| Language                | Python 3.x                |
| Key Libraries           | uvicorn, pydantic, pandas, requests |
| AI & Data Generation    | Groq API (product gen), LLM API (chat) |

---

## 📁 Directory Structure

```bash
.
├── images                   # Icons, Background, Demonstration Images, Database Visuals
│   ├── Icon
│   ├── background
│   ├── demo
│   └── database_images
├── backend                  # Core backend logic and APIs
│   ├── analytics.py             # Food data analytics functions
│   ├── chat_engine.py           # Conversational AI engine
│   ├── database_reader.py       # Read operations for SQLite/JSON data
│   ├── database_writer.py       # Write/update operations for databases
│   ├── filter_functions.py      # Filtering and recommendation logic
│   ├── main.py                  # Entry point for backend server
│   ├── session_id_generator.py  # Session ID Generator
│   └── models.py                # Data models and schemas
├── data                         # Databases and JSON datasets
│   ├── Analytics.db
│   ├── FoodData.db
│   ├── FoodData.json
│   └── __init__.py
├── frontend                 # Frontend app interface
│   └── app.py
├── sqlite                   # SQLite utilities and executables
│   ├── sqldiff.exe
│   ├── sqlite3.exe
│   ├── sqlite3_analyzer.exe
│   └── sqlite_rsync.exe
├── task                     # Documentation and project notes
│   └── AI Food Agent.pdf
└── requirements.txt         # Python dependencies
```

---

## 🛠 Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Kratugautam99/Foodie-Guru-Agent-Project.git
   cd Foodie-Guru-Agent-Project
   ```

2. **Create a virtual environment (by Conda) **
  ```bash
  conda env create -f environment.yml
  ```

3. **Set environment variable (Important)**
   ```bash
   export GROQ_API_KEY = "your_api_key_here"
   ```
---

## ▶️ Running the Project

### 1. Start the FastAPI Backend
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger UI will be available at `http://localhost:8000/docs`.

### 2. Directly Launch the Streamlit Frontend
```bash
streamlit run frontend/app.py
```
Open the Streamlit app in your browser at `http://localhost:8501` (or use the live demo link above).

----

## ✒️ Prompts Engineering Aid with Examples

### **1. General Inquiries**  
- "Tell me about pizza options."  
- "Tell me 10 options of pizzas."  
- "List the beverages."  
- "Tell me about beverages."  


### **2. Filter-Based Search**  
- "Show me pizzas with max spice level 5."  
- "Show me pizzas under $12."  
- "Show me vegetarian pizzas."  
- "Show me items with ingredients: mushrooms, olives."  


### **3. Ordering & Confirmation**  
- "Pack the buffalo ranch chicken pizza."  
- "Add the Classic Margherita Pizza to my order."  
- "Confirm my order."  
- "Pack the Truffle Mushroom Gourmet Pizza."  


### **4. Personalization & Preferences**  
- "Show me items for mood: happy."  
- "Show me items with dietary preference: low-carb."  
- "Show me items with allergens: peanuts."  
- "Show me items with ingredients: basil, tomatoes."  


### **5. Combined Filters**  
- "Show me pizzas with max spice 5, min price $10, popularity > 85."  
- "Show me beverages with max price $5, calories < 200, vegan."  
- "Show me items with ingredients: cheese, tomato, basil, and no nuts."  
- "Show me items with ingredients: cheese, tomato, basil, and no dairy."  

---

## 📖 API Endpoints

| Method | Endpoint           | Description                          |
|--------|--------------------|--------------------------------------|
| POST   | `/chat`            | Send user message, receive recommendations and updated interest score. |
| GET    | `/`       | {"message":"FoodieBot API is running!"} |

Full documentation is available via Swagger UI:  
http://localhost:8000/docs

---

## 🔧 Customization

- **Database**: Swap SQLite for PostgreSQL or MongoDB by updating `database_reader.py` / `database_writer.py` and installing the appropriate driver.
- **AI Model**: Change LLM API (Grok, Hugging Face, Gemini, Ollama) endpoints in `chat_engine.py`.
- **Analytics Storage**: Modify `Analytics.db` schema or use an external analytics service.

---

## 🤝 Contributing

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/YourFeature`)  
3. Commit your changes (`git commit -m "Add YourFeature"`)  
4. Push to your fork (`git push origin feature/YourFeature`)  
5. Open a Pull Request — i’ll review and merge!

---

## 📄 License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">
  Developed with 🧠 by <b>Kratu Gautam</b> | AIML Engineer<br>
  <a href="https://github.com/Kratugautam99">GitHub</a> | 
  <a href="https://kratugautam-foodieguruagent-project.streamlit.app">Streamlit[Frontend]</a> | 
  <a href="http://localhost:8000">FastAPI[Backend]</a>
</div>
