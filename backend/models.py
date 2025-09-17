from pydantic import BaseModel
from typing import List, Optional

class Fastfood(BaseModel):
    """Model for a Fastfood, matching the database schema."""
    product_id: str
    name: str
    category: str
    description: Optional[str] = None
    ingredients: Optional[str] = None
    price: float
    calories: Optional[int] = None
    prep_time: Optional[str] = None
    dietary_tags: Optional[str] = None
    mood_tags: Optional[str] = None
    allergens: Optional[str] = None
    popularity_score: Optional[int] = None
    chef_special: bool = False
    limited_time: bool = False
    spice_level: Optional[int] = None
    image_prompt: Optional[str] = None

    class Config:
        from_attributes = True # Important for returning data from DB

class ChatMessage(BaseModel):
    """Model for a message in the conversation."""
    message: str
    session_id: Optional[str] = None # To keep track of different conversations

class BotResponse(BaseModel):
    """Model for the bot's response."""
    reply: str
    suggested_fastfoods: List[Fastfood]=[] # List of fastfoods to recommend
    interest_score: int = 0
    session_id: str