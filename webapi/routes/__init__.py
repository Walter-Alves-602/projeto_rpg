from .auth import router as auth_router
from .user import router as user_router
from .mesa import router as mesa_router
from .personagem import router as personagem_router
from .criar_personagem import router as criar_personagem_router

__all__ = [
    "auth_router",
    "user_router",
    "mesa_router",
    "personagem_router",
    "criar_personagem_router"
]
