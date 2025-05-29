from typing import Optional

from src.infrastructure.repositories.habilidades_raciais_repository import IHabilidadesRaciaisRepository
from src.infrastructure.adapters.data_files.habilidades_raciais_data import HABILIDADES_RACIAIS_DATA

class HabilidadesRaciaisFileAdapter(IHabilidadesRaciaisRepository):
    def get_habilidade_descricao(self, nome_habilidade: str) -> Optional[str]:
        """
        Retorna a descrição de uma habilidade racial do dicionário de dados.
        """
        return HABILIDADES_RACIAIS_DATA.get(nome_habilidade)