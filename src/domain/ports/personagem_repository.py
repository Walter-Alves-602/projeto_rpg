# src/infrastructure/repositories/personagem_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.personagem import Personagem

class IPersonagemRepository(ABC):
    @abstractmethod
    def save(self, personagem: Personagem) -> None:
        """
        Salva ou atualiza um personagem no repositório.
        """
        pass

    @abstractmethod
    def get_by_name(self, nome: str) -> Optional[Personagem]:
        """
        Retorna um personagem pelo nome, ou None se não encontrado.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Personagem]:
        """
        Retorna todos os personagens salvos.
        """
        pass

    @abstractmethod
    def delete(self, nome: str) -> None:
        """
        Deleta um personagem pelo nome.
        """
        pass

    @abstractmethod
    def create_new_habilidade(self, nome: str, habilidade_nova: str):
        """
        Adiciona uma nova habilidade extra a um personagem existente.
        """
        pass
    