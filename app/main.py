from fastapi import FastAPI
from app.database import database
from app.routes import auth, payments # import the new routes

app = FastAPI(
    title="Payment Gateway API",
    description="Building Payment Gateway",
    version="1.0.0"
)

# Register the auth routes
app.include_router(auth.router) 
app.include_router(payments.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/db-check")
async def db_check():
    # A simple command to ping the MongoDB server
    await database.command("ping")
    return {"database_status": "connected successfully"}

