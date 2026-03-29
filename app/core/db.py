import os

from sqlalchemy import create_engine

from app.models.models import Base
from app.seed.seed_data import seed_data

DB_DIR = os.path.join("app", "db")
DB_PATH = os.path.join(DB_DIR, "movies.db")

os.makedirs(DB_DIR, exist_ok=True)

engine = create_engine(
    f"sqlite:///./{DB_PATH}", echo=True, connect_args={"check_same_thread": False}
)


def init_db():
    Base.metadata.create_all(engine)
    seed_data(engine=engine)
