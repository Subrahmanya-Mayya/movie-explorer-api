from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_movie_service
from app.schemas.schemas import (
    MovieDetailResponse,
    MovieListResponse,
    MovieReviewsResponse,
    NotFoundResponse,
)
from app.services.movie_service import MovieService

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=list[MovieListResponse])
def fetch_movies(
    genre: str = None,
    actor: str = None,
    director: str = None,
    release_year: Optional[int] = Query(
        None, ge=1950, description="Filter by release year"
    ),
    service: MovieService = Depends(get_movie_service),
):
    return service.fetch_movies(
        genre=genre,
        actor=actor,
        director=director,
        release_year=release_year,
    )


@router.get(
    "/{movie_id}",
    response_model=MovieDetailResponse,
    responses={404: {"model": NotFoundResponse, "description": "Movie not found"}},
)
def get_movie_detail(movie_id: int, service: MovieService = Depends(get_movie_service)):
    return service.get_movie_detail(movie_id)


@router.get(
    "/{movie_id}/reviews",
    response_model=MovieReviewsResponse,
    responses={404: {"model": NotFoundResponse, "description": "Movie not found"}},
)
def get_movie_reviews(
    movie_id: int, service: MovieService = Depends(get_movie_service)
):
    return service.get_movie_reviews(movie_id)
