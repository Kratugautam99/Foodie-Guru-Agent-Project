# main api for backend
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from .models import ChatMessage, BotResponse
from .chat_engine import analyze_message
from .session_id_generator import session_id

app = FastAPI(title="FoodieBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/chat", response_model=BotResponse)
async def chat_with_bot(message: ChatMessage):
    """The main endpoint for the chat conversation."""
    try:
        # Generate a session ID if it's the first message
        session_id = message.session_id or session_id
        # Get the response from the chat engine
        response_data = analyze_message(message.message, session_id)
        response_data["session_id"] = session_id
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "FoodieBot API is running!"}