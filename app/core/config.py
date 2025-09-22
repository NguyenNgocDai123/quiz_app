import os
from dotenv import load_dotenv

# Load file .env
load_dotenv()

# Lấy DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")