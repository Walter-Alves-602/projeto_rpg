from typing import List, Optional
from src.domain.models.armas import Arma, ArmaCorpoACorpo, ArmaDeAtaqueDistancia
from src.domain.ports.i_arma_repository import IArmaRepository
from .armas_data import ARMAS_DATA

class ArmaFileAdapter(IArmaRepository):
    def __init__(self):
        self._armas_data = ARMAS_DATA

    def _criar_objeto_arma(self, nome: str, data: dict) -> Arma:
        """Cria uma instância de Arma a partir dos dados."""
        if data["tipo"] == "corpo_a_corpo":
            return ArmaCorpoACorpo(
                nome=nome,
                custo=data["custo"],
                dano=data["dano"],
                tipo_dano=data["tipo_dano"],
                peso=data["peso"],
                propriedades=data.get("propriedades"),
                marcial=data.get("marcial", False),
            )
        elif data["tipo"] == "distancia":
            return ArmaDeAtaqueDistancia(
                nome=nome,
                custo=data["custo"],
                dano=data["dano"],
                tipo_dano=data["tipo_dano"],
                peso=data["peso"],
                alcance=data["alcance"],
                municao=data.get("municao"),
                propriedades=data.get("propriedades"),
                marcial=data.get("marcial", False),
            )
        raise ValueError(f"Tipo de arma desconhecido: {data['tipo']}")

    def get_by_name(self, nome: str) -> Optional[Arma]:
        data = self._armas_data.get(nome)
        return self._criar_objeto_arma(nome, data) if data else None

    def get_all(self) -> List[Arma]:
        return [self._criar_objeto_arma(nome, data) for nome, data in self._armas_data.items()]