from fastapi import APIRouter, Depends

from app.api.deps import get_genre_service
from app.schemas.schemas import GenreResponse
from app.services.genre_service import GenreService

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get("/", response_model=list[GenreResponse])
def get_genres(service: GenreService = Depends(get_genre_service)):
    return service.get_all_genres()
