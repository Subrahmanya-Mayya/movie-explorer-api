from sqlalchemy.orm import Session
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///./movies.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

def get_db():
    with Session(engine) as session:
        yield session