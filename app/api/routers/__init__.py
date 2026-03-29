from .actors import router as actors_router
from .directors import router as directors_router
from .genres import router as genres_router
from .movies import router as movies_router

__all__ = ["actors_router", "directors_router", "genres_router", "movies_router"]
