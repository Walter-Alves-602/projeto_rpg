from abc import ABC, abstractmethod


class RacaRepositoryPort(ABC):
    @abstractmethod
    def get_raca(self, nome_raca: str) -> dict:
        """
        Retorna os dados de uma raça específica.
        """
        pass