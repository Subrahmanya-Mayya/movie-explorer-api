from fastapi import FastAPI, APIRouter
from app.models.models import Base
from app.core.db import engine
from app.api import movies, genres, actors, directors
from app.seed.seed_data import seed_data

app = FastAPI(title="Movie Explorer API")

# Remove this later
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
# Remove this later
seed_data(engine=engine)

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(movies.router)
v1_router.include_router(genres.router)
v1_router.include_router(actors.router)
v1_router.include_router(directors.router)
app.include_router(v1_router)

@app.get("/")
def root():
    return {
        "message": "Movie Explorer API running"
    }