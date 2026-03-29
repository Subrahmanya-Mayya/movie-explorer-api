from sqlalchemy.orm import Session

from app.models.models import Director
from app.repositories.base_repository import BaseRepository


class DirectorRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db=db, model=Director)
