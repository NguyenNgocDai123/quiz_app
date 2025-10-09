import os
from dotenv import load_dotenv

# Lấy thư mục app/ từ file config.py (nếu config.py nằm trong app/core/)
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # core/ -> app/
dotenv_path = os.path.join(basedir, ".env")  # .env nằm trong app/

load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL chưa được set trong .env")