from fastapi import APIRouter

from app.api.routers import (
    actors_router,
    directors_router,
    genres_router,
    movies_router,
)

api_router = APIRouter(prefix="/v1")
api_router.include_router(movies_router)
api_router.include_router(genres_router)
api_router.include_router(actors_router)
api_router.include_router(directors_router)
