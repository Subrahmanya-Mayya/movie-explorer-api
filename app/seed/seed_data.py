from sqlalchemy.orm import Session
import random

from app.models.models import Actor, Director, Genre, Movie, Review


# Seed data for testing and development
def seed_data(engine):
    with Session(engine) as session:
        if session.query(Movie.id).first() is not None:
            return

        directors = [
            Director(name="Christopher Nolan"),
            Director(name="Quentin Tarantino"),
            Director(name="Steven Spielberg"),
        ]

        actors = [
            Actor(name="Leonardo DiCaprio"),
            Actor(name="Brad Pitt"),
            Actor(name="Tom Hanks"),
            Actor(name="Christian Bale"),
            Actor(name="Scarlett Johansson"),
        ]

        genres = [
            Genre(name="Action"),
            Genre(name="Drama"),
            Genre(name="Sci-Fi"),
            Genre(name="Thriller"),
            Genre(name="Comedy"),
        ]

        session.add_all(directors + actors + genres)
        session.commit()

        movie_data = {
            "Inception": "A thief who steals corporate secrets through dream-sharing technology is given a chance at redemption.",
            "Interstellar": "A team travels through a wormhole to find a new home for humanity as Earth faces collapse.",
            "Django Unchained": "A freed slave teams up with a bounty hunter to rescue his wife from a brutal plantation owner.",
            "The Dark Knight": "Batman battles the Joker, whose chaotic crimes push Gotham to the brink.",
            "Fight Club": "An insomniac office worker and a soap maker form an underground fight club that spirals out of control.",
            "Avengers": "Earth's mightiest heroes unite to stop a global threat and save the world.",
            "The Terminal": "A traveler becomes stranded in an airport terminal due to a sudden political crisis in his homeland.",
            "Shutter Island": "A U.S. marshal investigates a disappearance at a remote psychiatric facility with unsettling secrets.",
        }

        movies = []
        for title, synopsis in movie_data.items():
            movie = Movie(
                title=title,
                synopsis=synopsis,
                release_year=random.randint(2000, 2026),
                director=random.choice(directors),
            )

            movie.actors.extend(random.sample(actors, k=random.randint(2, 3)))

            movie.genres.extend(random.sample(genres, k=random.randint(1, 2)))

            session.add(movie)
            movies.append(movie)

        session.commit()

        review_comments = [
            "Excellent pacing and strong performances.",
            "Visually stunning and emotionally engaging.",
            "A bit long in places, but still very enjoyable.",
            "Great concept with memorable characters.",
            "Solid movie with a few weaker moments.",
            "Did not fully land for me, but had good scenes.",
            "A standout film I would watch again.",
        ]
        reviewer_names = [
            "Ava Johnson",
            "Liam Carter",
            "Noah Williams",
            "Mia Thompson",
            "Ethan Brown",
            "Sophia Miller",
            "Lucas Davis",
        ]

        for movie in movies:
            review_count = random.randint(2, 4)
            for _ in range(review_count):
                review = Review(
                    reviewer_name=random.choice(reviewer_names),
                    comment=random.choice(review_comments),
                    score=round(random.uniform(5.0, 9.8), 1),
                    movie=movie,
                )
                session.add(review)

        session.commit()
