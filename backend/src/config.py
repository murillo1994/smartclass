import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env caso exista
load_dotenv()

class Config:
    POSTGRES_DB = os.getenv("POSTGRES_DB", "smartclass_db")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "smartclass_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "smartclass_secret")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

    # Monta a DATABASE_URL caso não seja fornecida explicitamente
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    PORT = int(os.getenv("PORT", "5000"))
