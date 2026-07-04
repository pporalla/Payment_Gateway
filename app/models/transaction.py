from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: float          # in smallest currency unit (paise/cents)
    currency: str = "INR"
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: str
    user_id: str
    amount: float
    currency: str
    status: Literal["pending", "success", "failed", "refunded"]
    payment_intent_id: Optional[str] = None
    created_at: datetime