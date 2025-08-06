from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class SpellRepositoryPort(ABC):
    """Interface para repositórios de magias."""

    @abstractmethod
    def get_spell(self, spell_name: str) -> Optional[Dict[str, Any]]:
        """
        Retorna os dados completos de uma magia pelo seu nome.
        Retorna None se a magia não for encontrada.
        """
        pass

    @abstractmethod
    def get_all_spell_names(self) -> List[str]:
        """
        Retorna uma lista com os nomes de todas as magias disponíveis.
        """
        pass

    @abstractmethod
    def get_spells_by_level(self, level: int) -> List[Dict[str, Any]]:
        """
        Retorna uma lista de magias de um nível específico.
        """
        pass

    @abstractmethod
    def get_spells_by_class(self, class_name: str) -> List[Dict[str, Any]]:
        """
        Retorna uma lista de magias disponíveis para uma classe específica.
        """
        pass