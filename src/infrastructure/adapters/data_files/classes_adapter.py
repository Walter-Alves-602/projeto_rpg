from typing import Dict, Any, List

from src.domain.ports import ClasseRepositoryPort
from src.infrastructure.adapters.data_files.classes_data import _CLASSES_DATA

class ClasseFileAdapter(ClasseRepositoryPort):
    def get_classe(self, nome_classe: str) -> Dict[str, Any]:
        """Retorna os dados de uma classe pelo nome."""
        return _CLASSES_DATA.get(nome_classe, {})

    def get_pericias_por_classe(self, nome_classe: str) -> List[str]:
        """Retorna as perícias disponíveis para uma classe específica."""
        classe_data = self.get_classe(nome_classe)
        return classe_data.get("pericias_disponiveis", [])

    def get_all_classe_names(self) -> List[str]:
        """Retorna uma lista com os nomes de todas as classes disponíveis."""
        return list(_CLASSES_DATA.keys())
    