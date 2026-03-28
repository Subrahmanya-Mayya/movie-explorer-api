from typing import List, Optional
from pydantic import BaseModel


class MovieListResponse(BaseModel):
    id: int
    title: str
    release_year: int
    director: Optional[str]
    genres: List[str]

class MovieDetailResponse(BaseModel):
    id: int
    title: str
    release_year: int
    director: Optional[str]
    genres: List[str]
    actors: List[str]

class ActorResponse(BaseModel):
    id: int
    name: str


class ActorDetailResponse(BaseModel):
    id: int
    name: str
    movies: List[MovieListResponse]

class DirectorResponse(BaseModel):
    id: int
    name: str


class DirectorDetailResponse(BaseModel):
    id: int
    name: str
    movies: List[MovieListResponse]

class GenreResponse(BaseModel):
    id: int
    name: str