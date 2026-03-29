from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.models import Actor, Director, Genre, Movie, Review
from app.repositories.base_repository import BaseRepository


class MovieRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db=db, model=Movie)

    def list_movies(
        self,
        genre: Optional[str] = None,
        actor: Optional[str] = None,
        director: Optional[str] = None,
        release_year: Optional[int] = None,
    ) -> list[Movie]:
        stmt = select(Movie).order_by(Movie.release_year.desc())
        if genre:
            stmt = stmt.join(Movie.genres).where(Genre.name.ilike(f"%{genre}%"))
        if director:
            stmt = stmt.join(Movie.director).where(Director.name.ilike(f"%{director}%"))
        if actor:
            stmt = stmt.join(Movie.actors).where(Actor.name.ilike(f"%{actor}%"))
        if release_year:
            stmt = stmt.where(Movie.release_year == release_year)

        return self.db.execute(stmt.distinct()).scalars().all()

    def exists(self, movie_id: int) -> bool:
        return (
            self.db.execute(
                select(Movie.id).where(Movie.id == movie_id)
            ).scalar_one_or_none()
            is not None
        )

    def get_average_score(self, movie_id: int) -> Optional[float]:
        return self.db.execute(
            select(func.round(func.avg(Review.score), 2)).where(
                Review.movie_id == movie_id
            )
        ).scalar_one_or_none()

    def get_reviews(self, movie_id: int) -> list[Review]:
        return (
            self.db.execute(select(Review).where(Review.movie_id == movie_id))
            .scalars()
            .all()
        )
