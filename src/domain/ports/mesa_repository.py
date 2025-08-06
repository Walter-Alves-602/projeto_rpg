from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.models import Mesa


class MesaRepositoryPort(ABC):
    @abstractmethod
    def salvar(self, mesa: Mesa) -> None:
        ...

    @abstractmethod
    def buscar_por_id(self, mesa_id: str) -> Optional[Mesa]:
        ...

    @abstractmethod
    def listar_por_usuario_id(self, usuario_id: str) -> List[Mesa]:
        ...

    @abstractmethod
    def adicionar_jogador(self, mesa_id: str, usuario_id: str) -> None:
        ...

    @abstractmethod
    def remover_jogador(self, mesa_id: str, usuario_id: str) -> None:
        ...

    @abstractmethod
    def adicionar_mestre(self, mesa_id: str, usuario_id: str) -> None:
        ...

    @abstractmethod
    def adicionar_personagem(self, mesa_id: str, personagem_id: str) -> None:
        ...

    @abstractmethod
    def remover_personagem(self, mesa_id: str, personagem_id: str) -> None:
        ...
