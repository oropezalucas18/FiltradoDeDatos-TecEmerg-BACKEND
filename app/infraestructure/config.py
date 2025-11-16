import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()


class Settings:

    # ============================
    # JWT — Autenticación
    # ============================
    JWT_SECRET = os.getenv("JWT_SECRET", "changeme_supersecret")
    JWT_ALGORITHM = "HS256"


    # ============================
    # Firebase — Principal
    # ============================
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

    if not FIREBASE_CREDENTIALS:
        raise Exception("FIREBASE_CREDENTIALS no está definido en .env")


    # ============================
    # Supabase — Backup + Storage
    # ============================
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise Exception("SUPABASE_URL o SUPABASE_KEY no está definido en .env")

    SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "reportes")  # bucket para PDFs


    # ============================
    # RabbitMQ — Ingesta
    # ============================
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
    RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "sensor_ingest")


    # ============================
    # 🟩 Modo de ejecución
    # ============================
    ENV = os.getenv("ENV", "development")  # development | production


settings = Settings()
