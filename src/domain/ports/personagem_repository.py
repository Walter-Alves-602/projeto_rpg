from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.models.personagem import Personagem


class PersonagemRepositoryPort(ABC):
    @abstractmethod
    def salvar(self, personagem: Personagem) -> None:
        ...

    @abstractmethod
    def buscar_por_id(self, personagem_id: str) -> Optional[Personagem]:
        ...

    @abstractmethod
    def buscar_por_nome(self, nome: str) -> Optional[Personagem]:
        ...

    @abstractmethod
    def listar_todos(self) -> List[Personagem]:
        ...

    @abstractmethod
    def deletar(self, personagem_id: str) -> None:
        ...

    @abstractmethod
    def listar_por_ids(self, personagem_ids: List[str]) -> List[Personagem]:
        ...
    