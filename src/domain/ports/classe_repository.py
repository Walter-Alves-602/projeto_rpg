# src/infrastructure/repositories/classe_repository.py
from abc import ABC, abstractmethod

class IClasseRepository(ABC):
    @abstractmethod
    def get_classe(self, nome_classe: str) -> dict:
        """
        Retorna os dados de uma classe específica.
        """
        pass

    @abstractmethod
    def get_pericias_por_classe(self, nome_classe: str) -> list:
        """
        Retorna a lista de perícias disponíveis para uma classe específica.
        """
        pass
    