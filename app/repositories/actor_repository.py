from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.models import Actor, Genre, Movie
from app.repositories.base_repository import BaseRepository


class ActorRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db=db, model=Actor)

    def list_actors(
        self, movies: Optional[list[str]] = None, genres: Optional[list[str]] = None
    ) -> list[Actor]:
        stmt = select(Actor)
        if movies:
            stmt = stmt.join(Actor.movies).where(
                or_(*[Movie.title.ilike(f"%{movie}%") for movie in movies])
            )
        if genres:
            stmt = (
                stmt.join(Actor.movies)
                .join(Movie.genres)
                .where(or_(*[Genre.name.ilike(f"%{genre}%") for genre in genres]))
            )

        return self.db.execute(stmt.distinct()).scalars().all()
