from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.armas import Arma

class ArmaRepositoryPort(ABC):
    @abstractmethod
    def get_by_name(self, nome: str) -> Optional[Arma]:
        """Busca uma arma pelo nome."""
        pass

    @abstractmethod
    def get_all(self) -> List[Arma]:
        """Retorna uma lista de todas as armas."""
        pass