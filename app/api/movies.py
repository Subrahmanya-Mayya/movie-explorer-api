from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Movie,Genre, Actor, Director
from sqlalchemy import select, or_
from app.schemas.schemas import MovieDetailResponse, MovieListResponse

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/", response_model=list[MovieListResponse])
def fetch_movies(genre: list[str] = Query(None), actor: str = None, director: str = None, min_year: int= None, max_year: int = None, db: Session = Depends(get_db)):
    stmt = select(Movie)
    if genre:
        stmt = stmt.join(Movie.genres).where(
        or_(*[Genre.name.ilike(f"%{g}%") for g in genre])
    )
    if director:
        stmt = stmt.join(Movie.director).where(Director.name.ilike(f"%{director}%"))
    if actor:
        stmt = stmt.join(Movie.actors).where(Actor.name.ilike(f"%{actor}%"))
    # Check if the min max release year is needed.
    if min_year:
        stmt = stmt.where(Movie.release_year >= min_year)
    if max_year:
        stmt = stmt.where(Movie.release_year <= max_year)
    stmt = stmt.distinct()
    movies = db.execute(stmt).scalars().all()
    response = [
        {
            "id": m.id,
            "title": m.title,
            "release_year": m.release_year,
            "director": m.director.name if m.director else None,
            "genres": [g.name for g in m.genres]
        }
        for m in movies
    ]
    return response

@router.get("/{movie_id}", response_model=MovieDetailResponse)
def get_movie_detail(movie_id: int, db: Session = Depends(get_db)):
    stmt  = (
        select(Movie)
        .where(Movie.id == movie_id)
    )
    movie = db.execute(stmt).scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {
        "id": movie.id,
        "title": movie.title,
        "release_year": movie.release_year,
        "director": movie.director.name if movie.director else None,
        "genres": [g.name for g in movie.genres],
        "actors": [a.name for a in movie.actors],
    }