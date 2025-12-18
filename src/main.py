from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.models.db_helper import db_helper
from .api import router as api_router

from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)

origins = [
    "https://romberto.github.io",
    "http://localhost:5173",  # твой фронтенд
    "http://127.0.0.1:5173",  # иногда нужно
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # разрешаем все методы: GET, POST, OPTIONS и т.д.
    allow_headers=["*"],  # разрешаем все заголовки
)

main_app.include_router(api_router, prefix=settings.api.prefix)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:main_app", reload=True, host=settings.run.host, port=settings.run.port
    )
