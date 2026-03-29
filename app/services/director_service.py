from fastapi import HTTPException

from app.repositories.director_repository import DirectorRepository
from app.schemas.schemas import DirectorDetailResponse, DirectorResponse


class DirectorService:
    def __init__(self, repository: DirectorRepository):
        self.repository = repository

    def get_all_directors(self) -> list[DirectorResponse]:
        directors = self.repository.get_all()
        return [
            DirectorResponse(id=director.id, name=director.name)
            for director in directors
        ]

    def get_director_detail(self, director_id: int) -> DirectorDetailResponse:
        director = self.repository.get_by_id(director_id)
        if director is None:
            raise HTTPException(status_code=404, detail="Director not found")

        return DirectorDetailResponse(
            id=director.id, name=director.name, movies=list(director.movies)
        )
