import json
import os
from typing import List, Optional
from datetime import datetime
from src.schemas import UserCreate, Token, User, RequestEmail
from passlib.context import CryptContext

DATA_FILE = os.path.join('storage', 'users.json')



class UserRepository:
    def __init__(self):
        self.data_file = DATA_FILE
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _load_data(self) -> List[dict]:
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            data = []
        return data

    def _save_data(self, data):
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def get_user_by_id(self, user_id: int) -> Optional[dict]:
        users = self._load_data()
        user = next((user for user in users if user['id'] == user_id), None)
        return user

    async def get_user_by_username(self, username: str) -> Optional[dict]:
        users = self._load_data()
        user = next((user for user in users if user['username'] == username), None)
        return user

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        users = self._load_data()
        user = next((user for user in users if user['email'] == email), None)
        return user

    async def create_user(self, user_data: dict, avatar: str = None) -> dict:
        users = self._load_data()
        user_data = user_data.dict()  # конвертування Pydantic моделі у словник, якщо це ще не було зроблено
        user_data['id'] = max((user['id'] for user in users), default=0) + 1
        user_data['avatar'] = avatar
        user_data['confirmed'] = ''
        user_data['created_at'] = datetime.now().isoformat()
        user_data['updated_at'] = datetime.now().isoformat()
        users.append(user_data)
        self._save_data(users)
        return user_data

    async def confirmed_email(self, email: str) -> None:
        users = self._load_data()
        for user in users:
            if user['email'] == email:
                user['confirmed'] = True
                break
        self._save_data(users)

    async def update_avatar_url(self, email: str, url: str) -> Optional[dict]:
        users = self._load_data()
        user = next((user for user in users if user['email'] == email), None)
        if user:
            user['avatar'] = url
            self._save_data(users)
        return user
