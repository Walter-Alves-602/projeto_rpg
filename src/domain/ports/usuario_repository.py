from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models import Usuario


class UsuarioRepositoryPort(ABC):
    @abstractmethod
    def salvar(self, usuario: Usuario) -> None:
        ...

    @abstractmethod
    def buscar_por_username(self, username: str) -> Optional[Usuario]:
        ...

    @abstractmethod
    def buscar_por_mesa(mesa_id: str) -> Optional[Usuario]:
        ... 
    
    @abstractmethod
    def excluir_usuario(self, username: str) -> None:
        ...

    @abstractmethod
    def buscar_por_id(self, usuario_id: str) -> Optional[Usuario]:
        ...