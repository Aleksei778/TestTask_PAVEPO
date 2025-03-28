from dotenv import load_dotenv
import os

load_dotenv()

DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

YANDEX_CLIENT_ID = os.getenv("YANDEX_CLIENT_ID")
YANDEX_SECRET = os.getenv("YANDEX_SECRET")