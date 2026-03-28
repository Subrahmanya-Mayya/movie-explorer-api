from fastapi import APIRouter, Depends, HTTPException
from app.core.db import get_db
from app.models.models import Actor, Movie, Genre
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.schemas import ActorDetailResponse, ActorResponse

router = APIRouter(prefix="/actors", tags=["Actors"])

@router.get("/", response_model=list[ActorResponse])
def get_actors(movie: str = None, genre: str = None, db: Session = Depends(get_db)):
    stmt = select(Actor)
    if movie:
        stmt = stmt.join(Actor.movies).where(Movie.title.ilike(f"%{movie}%"))
    if genre:
        stmt = stmt.join(Actor.movies).join(Movie.genres).where(Genre.name.ilike(f"%{genre}%"))
    stmt = stmt.distinct()
    actors = db.execute(statement=stmt).scalars().all()
    return [
        {
            "id": a.id,
            "name": a.name
        }
        for a in actors
    ]

@router.get("/{actor_id}", response_model=ActorDetailResponse)
def get_actor_detail(actor_id: int, db: Session = Depends(get_db)):
    stmt = select(Actor).where(Actor.id == actor_id)
    actor = db.execute(statement=stmt).scalar_one_or_none()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return {
        "id": actor.id,
        "name": actor.name,
        "movies": [
            {
                "id": m.id,
                "title": m.title,
                "release_year": m.release_year
            }
            for m in actor.movies
        ]
    }