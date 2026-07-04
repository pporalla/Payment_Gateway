from app.models.transaction import TransactionCreate
from app.database import transactions_collection
from datetime import datetime
import stripe
from app.config import settings

# Tell the Stripe library to use your secret key
stripe.api_key = settings.stripe_secret_key

async def create_payment(payment: TransactionCreate, user_id: str) -> dict:
    # 1. Ask Stripe to create a Payment Intent
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(payment.amount), 
            currency=payment.currency.lower(),
            metadata={
                "user_id": user_id, 
                "description": payment.description
            }
        )
    except Exception as e:
        # If Stripe's servers reject the request, we catch the error
        raise ValueError(f"Stripe error: {str(e)}")

    # 2. Prepare the transaction document with the real Stripe data
    transaction_dict = {
        "user_id": user_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "description": payment.description,
        "status": "pending",
        "payment_intent_id": intent.id,          # e.g., pi_3M...
        "client_secret": intent.client_secret,   # e.g., pi_3M..._secret_...
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    # 3. Save the pending transaction to MongoDB
    result = await transactions_collection.insert_one(transaction_dict)
    
    return {
        "id": str(result.inserted_id),
        "user_id": transaction_dict["user_id"],
        "amount": transaction_dict["amount"],
        "currency": transaction_dict["currency"],
        "status": transaction_dict["status"],
        "payment_intent_id": transaction_dict["payment_intent_id"],
        "client_secret": transaction_dict["client_secret"],
        "created_at": transaction_dict["created_at"]
    }
async def refund_payment(transaction_id: str, user_id: str):
    # We will build the refund logic in a later milestone!
    pass