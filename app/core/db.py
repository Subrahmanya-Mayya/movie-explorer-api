from sqlalchemy import create_engine

from app.models.models import Base
from app.seed.seed_data import seed_data

engine = create_engine(
    "sqlite:///./movies.db", echo=True, connect_args={"check_same_thread": False}
)


def init_db():
    Base.metadata.create_all(engine)
    seed_data(engine=engine)
