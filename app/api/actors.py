from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.db import get_db
from app.models.models import Actor, Movie, Genre
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from app.schemas.schemas import ActorDetailResponse, ActorResponse, NotFoundResponse

router = APIRouter(prefix="/actors", tags=["Actors"])


@router.get("/", response_model=list[ActorResponse])
def get_actors(
    movies: list[str] = Query(None),
    genres: list[str] = Query(None),
    db: Session = Depends(get_db),
):
    stmt = select(Actor)
    if movies:
        stmt = stmt.join(Actor.movies).where(
            or_(*[Movie.title.ilike(f"%{m}%") for m in movies])
        )
    if genres:
        stmt = (
            stmt.join(Actor.movies)
            .join(Movie.genres)
            .where(or_(*[Genre.name.ilike(f"%{g}%") for g in genres]))
        )
    stmt = stmt.distinct()
    actors = db.execute(statement=stmt).scalars().all()
    return [ActorResponse(id=a.id, name=a.name) for a in actors]


@router.get(
    "/{actor_id}",
    response_model=ActorDetailResponse,
    responses={404: {"model": NotFoundResponse, "description": "Actor not found"}},
)
def get_actor_detail(actor_id: int, db: Session = Depends(get_db)):
    stmt = select(Actor).where(Actor.id == actor_id)
    actor = db.execute(statement=stmt).scalar_one_or_none()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return ActorDetailResponse(id=actor.id, name=actor.name, movies=list(actor.movies))
