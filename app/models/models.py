from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

class Base(DeclarativeBase):
    pass

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

class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    release_year: Mapped[int] = mapped_column()
    director_id: Mapped[int] = mapped_column(ForeignKey("directors.id"))
    director: Mapped["Director"] = relationship(back_populates="movies")
    actors: Mapped[list["Actor"]] = relationship(back_populates="movies", secondary=movie_actor)
    genres: Mapped[list["Genre"]] = relationship(back_populates="movies", secondary=movie_genre)

    def __repr__(self):
        return (
            f"<Movie(id={self.id}, "
            f"title='{self.title}', "
            f"year={self.release_year}, "
            f"director='{self.director.name if self.director else None}', "
            f"actors={[a.name for a in self.actors]}, "
            f"genres={[g.name for g in self.genres]})>"
        )

class Director(Base):
    __tablename__ = "directors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    movies: Mapped[list["Movie"]] = relationship(back_populates="director")

class Actor(Base):
    __tablename__ = "actors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    movies: Mapped[list["Movie"]] = relationship(back_populates="actors", secondary=movie_actor)

class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    movies: Mapped[list["Movie"]] = relationship(back_populates="genres", secondary=movie_genre)