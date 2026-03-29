from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import engine
from app.repositories.actor_repository import ActorRepository
from app.repositories.director_repository import DirectorRepository
from app.repositories.genre_repository import GenreRepository
from app.repositories.movie_repository import MovieRepository
from app.services.actor_service import ActorService
from app.services.director_service import DirectorService
from app.services.genre_service import GenreService
from app.services.movie_service import MovieService


def get_db():
    with Session(engine) as session:
        yield session


def get_movie_service(db: Session = Depends(get_db)) -> MovieService:
    return MovieService(repository=MovieRepository(db=db))


def get_actor_service(db: Session = Depends(get_db)) -> ActorService:
    return ActorService(repository=ActorRepository(db=db))


def get_director_service(db: Session = Depends(get_db)) -> DirectorService:
    return DirectorService(repository=DirectorRepository(db=db))


def get_genre_service(db: Session = Depends(get_db)) -> GenreService:
    return GenreService(repository=GenreRepository(db=db))
