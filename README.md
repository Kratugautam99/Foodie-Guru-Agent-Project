<p align="center">
  <img src="https://raw.githubusercontent.com/Kratugautam99/FoodieGuruAgent-Project/refs/heads/main/Images/Icon/icon.png" alt="FoodieGuruAgent Logo" width="400" />
  <h1 align="center">FoodieGuruAgent</h1>
  <p align="center">
    🍔 Your AI-powered culinary companion — delivering smart, mood‑aware, and personalized fast‑food recommendations in real time 🚀
  </p>
</p>

**FoodieGuruAgent** isn’t just another chatbot — it’s a full‑stack, agent‑driven food discovery experience.  
It listens like a friend, thinks like a data scientist, and recommends like a seasoned foodie.  
Powered by a **FastAPI** backend and a sleek **Streamlit** frontend, it taps into a curated **SQLite** database of 100+ AI‑generated menu items to serve you the perfect bite, every time.

Whether you’re craving a midnight burger, looking for vegan pizza, or just curious about what fits your budget and mood, FoodieGuruAgent blends **natural conversation**, **real‑time analytics**, and **smart filtering** to make every recommendation feel tailor‑made.  
From mood detection to interest scoring, from database queries to live dashboards — it’s your personal food concierge, available 24/7.

---


## 🚀 Live Demo

- Frontend Chat Interface (Streamlit):  
  https://kratugautam-foodieguruagent-project.streamlit.app

- Backend API (FastAPI):  
  http://13.51.79.106:8000

---

## ✨ Key Features

- **Natural Dialogue**  
  Understands user intent, moods, dietary needs, and price constraints.

- **Dynamic Interest Scoring**  
  Calculates a real-time “interest score” (0–100%) based on engagement signals (enthusiasm, order intent, budget mentions, etc.).

- **Smart Product Recommendations**  
  Filters and ranks items by mood tags, dietary tags, price range, popularity score, and real-time availability.

- **Database-Driven Responses**  
  Queries a SQLite database of 100+ AI-generated fast-food products across 10 categories (Burgers, Pizza, Tacos, Desserts, and more).

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
├── images
│   ├── Icon
│   ├── background
│   └── database_images
├── backend
│   ├── __init__.py
│   ├── analytics.py
│   ├── chat_engine.py
│   ├── database_reader.py
│   ├── database_writer.py
│   ├── filter_functions.py
│   ├── main.py
│   └── models.py
├── data
│   ├── Analytics.db
│   ├── FoodData.db
│   ├── FoodData.json
│   └── __init__.py
├── frontend
│   └── app.py
├── sqlite
│   ├── sqldiff.exe
│   ├── sqlite3.exe
│   ├── sqlite3_analyzer.exe
│   └── sqlite_rsync.exe
├── task
│   └── AI Food Agent.pdf
└── requirements.txt
```

---

## 🛠 Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Kratugautam99/FoodieGuruAgent-Project.git
   cd FoodieGuruAgent-Project
   ```

2. **Create a virtual environment**  
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional)  
   ```bash
   export API_URL="http://13.51.79.106:8000"
   ```
   Or add to `~/.bash_profile` for persistence:
   ```bash
   echo 'export API_URL="http://13.51.79.106:8000"' >> ~/.bash_profile
   source ~/.bash_profile
   ```

---

## ▶️ Running the Project

### 1. Start the FastAPI Backend
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger UI will be available at `http://<EC2_PUBLIC_IP>:8000/docs`.

### 2. Launch the Streamlit Frontend
```bash
cd ../frontend
streamlit run app.py
```
Open the Streamlit app in your browser at `http://localhost:8501` (or use the live demo link above).

---

## 📖 API Endpoints

| Method | Endpoint           | Description                          |
|--------|--------------------|--------------------------------------|
| POST   | `/chat`            | Send user message, receive recommendations and updated interest score. |
| GET    | `/analytics`       | Retrieve conversation analytics data. |

Full documentation is available via Swagger UI:  
http://13.51.79.106:8000/docs

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
5. Open a Pull Request — we’ll review and merge!

---

---

<div align="center">
  Developed with 🧠 by <b>Kratu Gautam</b> | AIML Engineer<br>
  <a href="https://github.com/Kratugautam99">GitHub</a> | 
  <a href="https://kratugautam-foodieguruagent-project.streamlit.app">Streamlit Frontend</a> | 
  <a href="http://13.51.79.106:8000">FastAPI Backend</a>
</div>


## 📄 License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
