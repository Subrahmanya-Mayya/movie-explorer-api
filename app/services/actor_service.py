from typing import Optional

from fastapi import HTTPException

from app.repositories.actor_repository import ActorRepository
from app.schemas.schemas import ActorDetailResponse, ActorResponse


class ActorService:
    def __init__(self, repository: ActorRepository):
        self.repository = repository

    def get_actors(
        self, movies: Optional[list[str]] = None, genres: Optional[list[str]] = None
    ) -> list[ActorResponse]:
        actors = self.repository.list_actors(movies=movies, genres=genres)
        return [ActorResponse(id=actor.id, name=actor.name) for actor in actors]

    def get_actor_detail(self, actor_id: int) -> ActorDetailResponse:
        actor = self.repository.get_by_id(actor_id)
        if actor is None:
            raise HTTPException(status_code=404, detail="Actor not found")

        return ActorDetailResponse(
            id=actor.id, name=actor.name, movies=list(actor.movies)
        )
