import uuid
from typing import Dict, List

from pydantic import BaseModel, Field


class Personagem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nome: str
    jogador: str
    raca_nome: str
    classe_nome: str
    nivel: int = 1
    pontos_de_experiencia: int = 0

    # Atributos base (após modificadores de raça já aplicados pelo Use Case)
    forca: int
    destreza: int
    constituicao: int
    inteligencia: int
    sabedoria: int
    carisma: int

    # Atributos derivados
    pontos_de_vida_max: int
    pontos_de_vida_atual: int
    deslocamento: float

    # Listas de proficiências, habilidades, etc.
    habilidades_raciais: List[str] = Field(default_factory=list)
    habilidades_extras: List[str] = Field(default_factory=list)
    proficiencias_armas: List[str] = Field(default_factory=list)
    proficiencias_armaduras: List[str] = Field(default_factory=list)
    testes_de_resistencia: List[str] = Field(default_factory=list)
    pericias_escolhidas: List[str] = Field(default_factory=list)
    inventario: List[str] = Field(default_factory=list)
    linguas: List[str] = Field(default_factory=list)
    ferramentas: List[str] = Field(default_factory=list)

    # Propriedade para calcular modificadores dinamicamente
    @property
    def modificadores_atributo(self) -> Dict[str, int]:
        atributos = {
            "forca": self.forca, "destreza": self.destreza, "constituicao": self.constituicao,
            "inteligencia": self.inteligencia, "sabedoria": self.sabedoria, "carisma": self.carisma
        }
        return {attr: (value - 10) // 2 for attr, value in atributos.items()}

    class Config:
        orm_mode = True