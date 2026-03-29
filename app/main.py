from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.api import movies, genres, actors, directors
from app.core.db import engine
from app.models.models import Base
from app.seed.seed_data import seed_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    seed_data(engine=engine)
    yield


app = FastAPI(title="Movie Explorer API", lifespan=lifespan)

origins = [
    "http://localhost:5173",  # Front end app
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(movies.router)
v1_router.include_router(genres.router)
v1_router.include_router(actors.router)
v1_router.include_router(directors.router)
app.include_router(v1_router)
