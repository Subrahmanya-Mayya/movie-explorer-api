from sqlalchemy.orm import Session
import random

from models import Actor, Director, Genre, Movie

def seed_data(engine):
    with Session(engine) as session:

        # --- Directors ---
        directors = [
            Director(name="Christopher Nolan"),
            Director(name="Quentin Tarantino"),
            Director(name="Steven Spielberg"),
        ]

        # --- Actors ---
        actors = [
            Actor(name="Leonardo DiCaprio"),
            Actor(name="Brad Pitt"),
            Actor(name="Tom Hanks"),
            Actor(name="Christian Bale"),
            Actor(name="Scarlett Johansson"),
        ]

        # --- Genres ---
        genres = [
            Genre(name="Action"),
            Genre(name="Drama"),
            Genre(name="Sci-Fi"),
            Genre(name="Thriller"),
            Genre(name="Comedy"),
        ]

        session.add_all(directors + actors + genres)
        session.commit()

        # --- Movies ---
        movie_titles = [
            "Inception", "Interstellar", "Django Unchained",
            "The Dark Knight", "Fight Club", "Avengers",
            "The Terminal", "Shutter Island"
        ]

        for title in movie_titles:
            movie = Movie(
                title=title,
                release_year=random.randint(2000, 2023),
                director=random.choice(directors)
            )

            # random actors (2–3)
            movie.actors.extend(random.sample(actors, k=random.randint(2, 3)))

            # random genres (1–2)
            movie.genres.extend(random.sample(genres, k=random.randint(1, 2)))

            session.add(movie)

        session.commit()