from sqlalchemy.orm import Session

from app.models.models import Genre
from app.repositories.base_repository import BaseRepository


class GenreRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db=db, model=Genre)
