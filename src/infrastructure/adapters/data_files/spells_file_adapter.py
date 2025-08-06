# src/infrastructure/adapters/data_files/spells_file_adapter.py
from typing import Any, Dict, List, Optional

from src.domain.ports import SpellRepositoryPort
from src.infrastructure.adapters.data_files.spells_data import \
    _SPELLS_DATA  # Importa os dados das magias


class SpellFileAdapter(SpellRepositoryPort):
    """
    Adaptador para acessar dados de magias a partir de um arquivo de dados estático.
    Implementa a interface ISpellRepository.
    """

    def _add_name_to_spell_data(self, name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método auxiliar para adicionar o nome da magia ao dicionário de dados da magia.
        Cria uma cópia do dicionário original para evitar modificações indesejadas nos dados estáticos.
        """
        spell_with_name = data.copy()
        spell_with_name["nome"] = name
        return spell_with_name

    def get_spell(self, spell_name: str) -> Optional[Dict[str, Any]]:
        """
        Retorna os dados completos de uma magia pelo seu nome.
        Retorna None se a magia não for encontrada.
        """
        spell_data = _SPELLS_DATA.get(spell_name)
        if spell_data:
            # Usa o método auxiliar para adicionar o nome antes de retornar
            return self._add_name_to_spell_data(spell_name, spell_data)
        return None

    def get_all_spell_names(self) -> List[str]:
        """
        Retorna uma lista com os nomes de todas as magias disponíveis.
        """
        return list(_SPELLS_DATA.keys())

    def get_spells_by_level(self, level: int) -> List[Dict[str, Any]]:
        """
        Retorna uma lista de magias de um nível específico.
        """
        result = []
        # Itera sobre chaves (nomes) e valores (dados) do dicionário _SPELLS_DATA
        for name, spell_data in _SPELLS_DATA.items():
            if spell_data.get("nivel") == level:
                # Adiciona o nome ao dicionário de dados da magia
                result.append(self._add_name_to_spell_data(name, spell_data))
        return result

    def get_spells_by_class(self, class_name: str) -> List[Dict[str, Any]]:
        """
        Retorna uma lista de magias disponíveis para uma classe específica.
        Considera tanto classes diretamente listadas quanto a capitalização.
        """
        lower_class_name = class_name.lower()
        result = []
        # Itera sobre chaves (nomes) e valores (dados) do dicionário _SPELLS_DATA
        for name, spell_data in _SPELLS_DATA.items():
            # Verifica se a classe está na lista de classes da magia (case-insensitive)
            if lower_class_name in [c.lower() for c in spell_data.get("classes", [])]:
                # Adiciona o nome ao dicionário de dados da magia
                result.append(self._add_name_to_spell_data(name, spell_data))
        return result