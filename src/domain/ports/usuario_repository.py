from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models.usuario import Usuario


class UsuarioRepositoryPort(ABC):
    @abstractmethod
    def salvar(self, usuario: Usuario) -> None:
        ...

    @abstractmethod
    def buscar_por_username(self, username: str) -> Optional[Usuario]:
        ...
