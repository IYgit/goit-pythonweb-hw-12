import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from pathlib import Path
from urllib.parse import quote_plus

# Отримуємо шлях до кореня проєкту (hw10)
project_root = Path(__file__).resolve().parents[2]
# Формуємо шлях до .env
env_path = project_root / ".env"

# Завантажуємо .env
load_dotenv(dotenv_path=env_path)

required_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

def get_database_url():
    return str(
        URL.create(
            drivername="postgresql+asyncpg",
            username=os.getenv("DB_USER"),
            password=quote_plus(os.getenv("DB_PASSWORD")),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
        )
    )

# url = "postgresql://postgres:postgres_password@localhost:5432/postgres"
# engine = create_engine(url)
# with engine.connect() as conn:
#     print("Підключення успішне!")

# print(f"username: {os.getenv("DB_USER")}")
# print(f"password: {quote_plus(os.getenv("DB_PASSWORD"))}")
# print(f"host: {os.getenv("DB_HOST")}")
# print(f"port: {os.getenv("DB_PORT")}")
# print(f"database: {os.getenv("DB_NAME")}")

print(f"{get_database_url()}")




class Config:
    # DB_URL = "postgresql+asyncpg://postgres:postgres_password@localhost:5432/postgres"
    DB_URL = get_database_url()


config = Config
