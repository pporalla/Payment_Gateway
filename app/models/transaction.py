from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: float          # 91.50 like this
    currency: str = "INR"
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: str
    user_id: str
    amount: float
    currency: str
    status: Literal["pending", "success", "failed", "refunded"]
    payment_intent_id: Optional[str] = None
    client_secret: Optional[str] = None 
    created_at: datetime