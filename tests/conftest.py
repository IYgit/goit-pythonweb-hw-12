# tests/conftest.py
import os
import sys

# додаємо корінь проєкту (один рівень вище tests/) в sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import asyncio
from unittest.mock import MagicMock
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.database.models import Base, User, Contact
from src.database.db import get_db
from src.schemas import ContactModel
from src.services.auth import create_access_token, Hash

from src.repository.users import UserRepository as DBUserRepository # об'єкт, який треба підставити замість реалізованого UserRepository
import src.services.users as svc_mod  # модуль, в якому треба підставити об'єкт DBUserRepository

from main import app
# … решта фікстур …


DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)

test_user = {
    "username": "mom",
    "email": "mom@gmail.com",
    "password": "12345678",
    "role": "user",
}

user_data = {
    "username": "dad",
    "email": "dad@gmail.com",
    "password": "12345678",
    "role": "user",
}

user_data_unique_email = {
    "username": "dad",
    "email": "dady@gmail.com",
    "password": "12345678",
    "role": "user",
}

user_data_unique = {
    "username": "dady",
    "email": "dady@gmail.com",
    "password": "12345678",
    "role": "user",
}


@pytest.fixture
def user():
    return User(id=1, username="testuser", role="user")


@pytest.fixture
def contact(user: User):
    return Contact(
        id=1,
        name="Evan",
        surname="Jedi",
        email="evan@example.com",
        phone="111-222-3333",
        birthday="2002-02-02",
        user=user,
    )


@pytest.fixture
def contact_none():
    return None


@pytest.fixture
def contact_body():
    return ContactModel(
        name="Evan",
        surname="Jedi",
        email="evan@example.com",
        phone="111-222-3333",
        birthday="2002-02-02",
    )


@pytest.fixture(scope="module", autouse=True)
def init_models_wrap():
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async with TestingSessionLocal() as session:
            hash_password = Hash().get_password_hash(test_user["password"])
            current_user = User(
                username=test_user["username"],
                email=test_user["email"],
                password=hash_password,
                confirmed=True,
                avatar="https://twitter.com/gravatar.jpg",
                role=test_user["role"],
            )
            session.add(current_user)
            await session.commit()
            await session.refresh(current_user)
            test_user["id"] = current_user.id

    asyncio.run(init_models())


@pytest.fixture(scope="module")
def db_session():
    session = TestingSessionLocal()     # повертає AsyncSession, але створюється без await
    yield session
    session.rollback()
    session.close()



@pytest.fixture(scope="module")
def client(db_session):                    # db_session — теж мусить бути синхронною
    def override_get_db():                 # Тепер — звичайна деф‑функція, не async
        try:
            yield db_session               # і вона повертає реальний об'єкт Session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def patch_user_repo(monkeypatch, db_session):
    def get_db_user_repository(*args, **kwargs):
        return DBUserRepository(db_session)
    monkeypatch.setattr(svc_mod, "UserRepository", get_db_user_repository)


@pytest.fixture
def auth_headers():

    token = "test_token"
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def fake_upload_file():

    mock_file = MagicMock()
    mock_file.file = MagicMock()
    mock_file.filename = "avatar.png"
    return mock_file


@pytest.fixture(scope="module")
def event_loop():

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()



@pytest_asyncio.fixture()
async def get_token():
    token = await create_access_token(data={"sub": test_user["username"]})
    return token

