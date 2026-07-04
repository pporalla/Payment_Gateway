from fastapi import APIRouter, Depends
from app.models.transaction import TransactionCreate, TransactionResponse
from app.services.payment_service import create_payment, refund_payment
from app.utils.security import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/initiate", response_model=TransactionResponse)
async def initiate_payment(
    payment: TransactionCreate,
    current_user = Depends(get_current_user)
):
    return await create_payment(payment, current_user["id"])