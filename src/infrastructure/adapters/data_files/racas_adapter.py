# src/infrastructure/adapters/data_files/racas_adapter.py
from src.infrastructure.repositories.raca_repository import IRacaRepository

# O dicionário RACA original foi adaptado para ser parte do adaptador de dados
_RACA_DATA = {
    "Anão da Colina": {
        "atributos": {"constituicao": 2},
        "linguas": ["Comum", "Anão"]
    },
    "Anão da Montanha": {
        "atributos": {"forca": 2, "constituicao": 2},
        "linguas": ["Comum", "Anão"],
    },
    "Elfo Alto": {
        "atributos": {"inteligencia": 1, "destreza": 2},
        "linguas": ["Comum", "Elfico"],
    },
    # Outras raças podem ser adicionadas aqui
}

class RacaFileAdapter(IRacaRepository):
    def get_raca(self, nome_raca: str) -> dict:
        """
        Retorna os dados de uma raça do arquivo de dados.
        """
        return _RACA_DATA.get(nome_raca, {})