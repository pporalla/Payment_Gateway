from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    mongodb_url: str
    database_name: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    stripe_secret_key: str
    stripe_webhook_secret: str 

    class Config:
        env_file = ".env"
        extra = "ignore" # <--- Adding this prevents future "extra" errors

settings = Settings()
