from fastapi import FastAPI
import uvicorn
from src.api import contacts, utils, auth, users
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Дозволяє всім доменам
    allow_credentials=True,
    allow_methods=["*"],  # Дозволяє всім методам
    allow_headers=["*"],  # Дозволяє всім заголовкам
)


app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
