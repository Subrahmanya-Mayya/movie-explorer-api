from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Movie, Genre, Actor, Director, Review
from sqlalchemy import func, select, or_
from app.schemas.schemas import (
    MovieDetailResponse,
    MovieListResponse,
    MovieReviewsResponse,
    ReviewResponse,
    NotFoundResponse,
)

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=list[MovieListResponse])
def fetch_movies(
    genre: str = None,
    actor: str = None,
    director: str = None,
    release_year: Optional[int] = Query(
        None, ge=1950, description="Filter by release year"
    ),
    db: Session = Depends(get_db),
):
    stmt = select(Movie).order_by(Movie.release_year.desc())
    if genre:
        stmt = stmt.join(Movie.genres).where(Genre.name.ilike(f"%{genre}%"))
    if director:
        stmt = stmt.join(Movie.director).where(Director.name.ilike(f"%{director}%"))
    if actor:
        stmt = stmt.join(Movie.actors).where(Actor.name.ilike(f"%{actor}%"))
    if release_year:
        stmt = stmt.where(Movie.release_year == release_year)
    stmt = stmt.distinct()
    movies = db.execute(stmt).scalars().all()
    return [
        MovieListResponse(
            id=m.id,
            title=m.title,
            release_year=m.release_year,
            director=m.director,
            genres=[g.name for g in m.genres],
        )
        for m in movies
    ]


@router.get(
    "/{movie_id}",
    response_model=MovieDetailResponse,
    responses={404: {"model": NotFoundResponse, "description": "Movie not found"}},
)
def get_movie_detail(movie_id: int, db: Session = Depends(get_db)):
    stmt = select(Movie).where(Movie.id == movie_id)
    movie = db.execute(stmt).scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    avg_score = db.execute(
        select(func.round(func.avg(Review.score), 2)).where(Review.movie_id == movie_id)
    ).scalar_one_or_none()

    return MovieDetailResponse(
        id=movie.id,
        title=movie.title,
        release_year=movie.release_year,
        synopsis=movie.synopsis,
        director=movie.director,
        genres=[g.name for g in movie.genres],
        actors=list(movie.actors),
        average_score=avg_score,
    )


@router.get(
    "/{movie_id}/reviews",
    response_model=MovieReviewsResponse,
    responses={404: {"model": NotFoundResponse, "description": "Movie not found"}},
)
def get_movie_reviews(movie_id: int, db: Session = Depends(get_db)):
    movie_exists = db.execute(
        select(Movie.id).where(Movie.id == movie_id)
    ).scalar_one_or_none()
    if not movie_exists:
        raise HTTPException(status_code=404, detail="Movie not found")

    avg_score = db.execute(
        select(func.round(func.avg(Review.score), 2)).where(Review.movie_id == movie_id)
    ).scalar_one_or_none()

    reviews = (
        db.execute(select(Review).where(Review.movie_id == movie_id)).scalars().all()
    )

    return MovieReviewsResponse(
        average_score=avg_score,
        reviews=list(reviews),
    )
