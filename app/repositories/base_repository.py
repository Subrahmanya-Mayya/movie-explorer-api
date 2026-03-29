from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Base


class BaseRepository:
    def __init__(self, db: Session, model: type[Base]):
        self.db = db
        self.model = model

    def get_all(self):
        return self.db.execute(select(self.model)).scalars().all()

    def get_by_id(self, entity_id: int):
        return self.db.execute(
            select(self.model).where(self.model.id == entity_id)
        ).scalar_one_or_none()
