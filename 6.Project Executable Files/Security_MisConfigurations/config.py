import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables (even if unsafe!)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_unsafe_secret")
    DEBUG = os.getenv("DEBUG", "True")  # Exposing Debug Mode
