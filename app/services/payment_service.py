from app.models.transaction import TransactionCreate
from app.database import transactions_collection
from datetime import datetime

async def create_payment(payment: TransactionCreate, user_id: str) -> dict:
    # Prepare the transaction document
    transaction_dict = {
        "user_id": user_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "description": payment.description,
        "status": "pending", # It starts as pending before Stripe confirms it
        "payment_intent_id": None, # We will add Stripe later
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    # Save to MongoDB
    result = await transactions_collection.insert_one(transaction_dict)
    
    # Return the response matching our TransactionResponse model
    return {
        "id": str(result.inserted_id),
        "user_id": transaction_dict["user_id"],
        "amount": transaction_dict["amount"],
        "currency": transaction_dict["currency"],
        "status": transaction_dict["status"],
        "payment_intent_id": transaction_dict["payment_intent_id"],
        "created_at": transaction_dict["created_at"]
    }

async def refund_payment(transaction_id: str, user_id: str):
    # We will build the refund logic in a later milestone!
    pass