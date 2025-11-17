import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FIREBASE_CREDENTIALS_PATH: str
    FIREBASE_PROJECT_ID: str = ""

    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_BUCKET: str = "reportes"

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    RABBITMQ_HOST: str
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_QUEUE: str

    SPARK_HOME: str = "/opt/spark"

    ENV: str = "dev"

    class Config:
        env_file = ".env"

settings = Settings()
