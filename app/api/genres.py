from fastapi import APIRouter, Depends
from app.core.db import get_db
from app.models.models import Genre
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.schemas import GenreResponse

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get("/", response_model=list[GenreResponse])
def get_genres(db: Session = Depends(get_db)):
    stmt = select(Genre)
    genres = db.execute(statement=stmt).scalars().all()
    return [GenreResponse(id=g.id, name=g.name) for g in genres]
