from fastapi import APIRouter, Depends

from app.api.deps import get_director_service
from app.schemas.schemas import (
    DirectorDetailResponse,
    DirectorResponse,
    NotFoundResponse,
)
from app.services.director_service import DirectorService

router = APIRouter(prefix="/directors", tags=["Directors"])


@router.get("/", response_model=list[DirectorResponse])
def get_genres(service: DirectorService = Depends(get_director_service)):
    return service.get_all_directors()


@router.get(
    "/{director_id}",
    response_model=DirectorDetailResponse,
    responses={404: {"model": NotFoundResponse, "description": "Director not found"}},
)
def get_director_detail(
    director_id: int, service: DirectorService = Depends(get_director_service)
):
    return service.get_director_detail(director_id)
