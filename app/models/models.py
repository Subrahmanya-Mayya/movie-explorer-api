from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    String,
    ForeignKey,
    Table,
    Column,
    Text,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship


class Base(DeclarativeBase):
    pass


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )


movie_actor = Table(
    "movie_actor",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("actor_id", ForeignKey("actors.id"), primary_key=True),
)

movie_genre = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)


class Movie(TimestampMixin, Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    synopsis: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    release_year: Mapped[int] = mapped_column()
    director_id: Mapped[int] = mapped_column(ForeignKey("directors.id"))
    director: Mapped["Director"] = relationship(back_populates="movies")
    actors: Mapped[list["Actor"]] = relationship(
        back_populates="movies", secondary=movie_actor
    )
    genres: Mapped[list["Genre"]] = relationship(
        back_populates="movies", secondary=movie_genre
    )
    reviews: Mapped[list["Review"]] = relationship(back_populates="movie")

    __table_args__ = (
        CheckConstraint("release_year >= 1900", name="check_release_year"),
    )

    def __repr__(self):
        return (
            f"<Movie(id={self.id}, "
            f"title='{self.title}', "
            f"year={self.release_year}, "
            f"director='{self.director.name if self.director else None}', "
            f"actors={[a.name for a in self.actors]}, "
            f"genres={[g.name for g in self.genres]})>"
        )


class Director(TimestampMixin, Base):
    __tablename__ = "directors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    movies: Mapped[list["Movie"]] = relationship(back_populates="director")


class Actor(TimestampMixin, Base):
    __tablename__ = "actors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    movies: Mapped[list["Movie"]] = relationship(
        back_populates="actors", secondary=movie_actor
    )


class Genre(TimestampMixin, Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    movies: Mapped[list["Movie"]] = relationship(
        back_populates="genres", secondary=movie_genre
    )


class Review(TimestampMixin, Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    reviewer_name: Mapped[str] = mapped_column(String(50), nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    movie: Mapped["Movie"] = relationship(back_populates="reviews")

    __table_args__ = (
        CheckConstraint("score >= 0.0 AND score <= 10.0", name="check_score_range"),
    )
