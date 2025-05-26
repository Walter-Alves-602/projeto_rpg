# src/infrastructure/adapters/data_files/classes_adapter.py
from src.infrastructure.repositories.classe_repository import IClasseRepository
from src.infrastructure.adapters.data_files.pericias_adapter import PERICIAS

# Dados de exemplo para as classes
_CLASSES_DATA = {
    "Barbaro": {
        "dado_de_vida": "1d12",
        "armas": ["Armas simples", "armas marciais"],
        "armaduras": ["Armadura leve", "Armadura média"],
        "testes_de_resistencia": ["Força", "Constituição"],
        "ferramentas": [],
        "quantidade_de_pericias": 2,
        "pericias_disponiveis_nomes": ["Adestrar Animais", "Atletismo", "Intimidação", "Natureza", "Percepção", "Sobrevivência"]
    },
    "Bardo": {
        "dado_de_vida": "1d8",
        "armas": ["Armas simples", "Bestas de Mão", "Espadas curtas", "Espadas longas", "Ra"],
        "armaduras": ["Armadura leve"],
        "testes_de_resistencia": ["Destreza", "Carisma"],
        "ferramentas": ["Três instrumentos musicais, à sua escolha"],
        "quantidade_de_pericias": 3,
        "pericias_disponiveis_nomes": list(PERICIAS.keys()) # Exemplo: Bardo pode escolher entre todas as perícias
    },
    # Adicionar outras classes aqui
}

class ClasseFileAdapter(IClasseRepository):
    def get_classe(self, nome_classe: str) -> dict:
        """
        Retorna os dados de uma classe do arquivo de dados.
        """
        return _CLASSES_DATA.get(nome_classe, {})

    def get_pericias_por_classe(self, nome_classe: str) -> list:
        """
        Retorna a lista de nomes de perícias disponíveis para uma classe específica.
        """
        classe_data = _CLASSES_DATA.get(nome_classe, {})
        return classe_data.get("pericias_disponiveis_nomes", [])