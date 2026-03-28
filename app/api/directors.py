from fastapi import APIRouter, Depends, HTTPException
from app.core.db import get_db
from app.models.models import Director
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.schemas import DirectorDetailResponse, DirectorResponse

router = APIRouter(prefix="/directors", tags=["Directors"])

@router.get("/", response_model=list[DirectorResponse])
def get_genres(db: Session = Depends(get_db)):
    stmt = select(Director)
    directors = db.execute(statement=stmt).scalars().all()
    return [
        {
            "id": d.id,
            "name": d.name
        }
        for d in directors
    ]

@router.get("/{director_id}", response_model=DirectorDetailResponse)
def get_director_detail(director_id: int, db: Session = Depends(get_db)):
    stmt = select(Director).where(Director.id == director_id)
    director = db.execute(statement=stmt).scalar_one_or_none()
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    return {
        "id": director.id,
        "name": director.name,
        "movies": [
            {
                "id": m.id,
                "title": m.title,
                "release_year": m.release_year
            }
            for m in director.movies
        ]
    }