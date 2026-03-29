from fastapi import APIRouter, Depends, Query

from app.api.deps import get_actor_service
from app.schemas.schemas import ActorDetailResponse, ActorResponse, NotFoundResponse
from app.services.actor_service import ActorService

router = APIRouter(prefix="/actors", tags=["Actors"])


@router.get("/", response_model=list[ActorResponse])
def get_actors(
    movies: list[str] = Query(None),
    genres: list[str] = Query(None),
    service: ActorService = Depends(get_actor_service),
):
    return service.get_actors(movies=movies, genres=genres)


@router.get(
    "/{actor_id}",
    response_model=ActorDetailResponse,
    responses={404: {"model": NotFoundResponse, "description": "Actor not found"}},
)
def get_actor_detail(actor_id: int, service: ActorService = Depends(get_actor_service)):
    return service.get_actor_detail(actor_id)
