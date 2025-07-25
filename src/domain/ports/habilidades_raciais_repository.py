from abc import ABC, abstractmethod
from typing import Optional

class IHabilidadesRaciaisRepository(ABC):
    @abstractmethod
    def get_habilidade_descricao(self, nome_habilidade: str) -> Optional[str]:
        """
        Retorna a descrição de uma habilidade racial dado o seu nome.
        Retorna None se a habilidade não for encontrada.
        """
        pass