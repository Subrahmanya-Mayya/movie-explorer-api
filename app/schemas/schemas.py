from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class NotFoundResponse(BaseModel):
    detail: str


class ActorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class DirectorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class MovieSimpleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    release_year: int


class MovieListResponse(BaseModel):
    id: int
    title: str
    release_year: int
    director: Optional[DirectorResponse]
    genres: List[str]


class MovieDetailResponse(BaseModel):
    id: int
    title: str
    release_year: int
    synopsis: Optional[str]
    director: Optional[DirectorResponse]
    genres: List[str]
    actors: List[ActorResponse]
    average_score: Optional[float]


class ActorDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    movies: List[MovieSimpleResponse]


class DirectorDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    movies: List[MovieSimpleResponse]


class GenreResponse(BaseModel):
    id: int
    name: str


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reviewer_name: str
    comment: Optional[str]
    score: float


class MovieReviewsResponse(BaseModel):
    average_score: Optional[float]
    reviews: List[ReviewResponse]
