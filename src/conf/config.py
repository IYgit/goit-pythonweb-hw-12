import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic import ConfigDict, EmailStr
from pydantic_settings import BaseSettings
from sqlalchemy.engine.url import URL

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
    """
    Формує URL для підключення до бази даних.

    Повертає:
    - str: URL для підключення до бази даних.
    """
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

print(f"{get_database_url()}")




class Config:
    DB_URL = get_database_url()


config = Config


class Settings(BaseSettings):
    """
    Клас конфігурації для налаштувань додатка.

    Цей клас автоматично завантажує налаштування з середовища або файлу `.env`, використовуючи бібліотеку Pydantic.

    Атрибути:
    - DB_URL (str): URL для підключення до бази даних.
    - JWT_SECRET (str): Секретний ключ для підпису JWT-токенів.
    - JWT_ALGORITHM (str): Алгоритм для генерації JWT-токенів (за замовчуванням: HS256).
    - JWT_EXPIRATION_SECONDS (int): Час життя токенів у секундах (за замовчуванням: 3600).
    - MAIL_USERNAME (EmailStr): Логін для SMTP сервера.
    - MAIL_PASSWORD (str): Пароль для SMTP сервера.
    - MAIL_FROM (EmailStr): Електронна адреса, від якої надсилаються листи.
    - MAIL_PORT (int): Порт для підключення до SMTP сервера.
    - MAIL_SERVER (str): Доменне ім'я SMTP сервера.
    - MAIL_FROM_NAME (str): Ім'я відправника для листів (за замовчуванням: "API Service").
    - MAIL_STARTTLS (bool): Чи використовувати STARTTLS для SMTP (за замовчуванням: False).
    - MAIL_SSL_TLS (bool): Чи використовувати SSL/TLS для SMTP (за замовчуванням: True).
    - USE_CREDENTIALS (bool): Чи використовувати облікові дані для SMTP (за замовчуванням: True).
    - VALIDATE_CERTS (bool): Чи перевіряти сертифікати SSL (за замовчуванням: True).
    - CLOUDINARY_NAME (str): Ім'я облікового запису Cloudinary.
    - CLOUDINARY_API_KEY (int): API-ключ для Cloudinary.
    - CLOUDINARY_API_SECRET (str): Секретний ключ для Cloudinary.

    Методи:
    - model_config: Конфігурація для завантаження налаштувань із файлу `.env`.

    Приклад використання:
    ```
    from src.conf.config import settings
    print(settings.DB_URL)
    ```
    """
    DB_URL: str = config.DB_URL

    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_SECONDS: int = 3600

    MAIL_USERNAME: EmailStr = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: EmailStr = os.getenv("MAIL_FROM")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME: str = "API Service"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    CLOUDINARY_NAME: str = os.getenv("CLOUDINARY_NAME")
    CLOUDINARY_API_KEY: int = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: str = os.getenv("CLOUDINARY_API_SECRET")

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
