from dataclasses import dataclass
from pericias import pericias

@dataclass
class Classes:
    dado_de_vida: str
    armas: list
    armaduras: list
    testes_de_resistencia: list
    ferramentas: list
    quantidade_de_pericias: int
    pericias: list = pericias.keys()


Barbaro = Classes(dado_de_vida="1d12",
    armas=["Armas simples", "armas marciais"],
    armaduras=["Armadura leve", "Armadura média"],
    testes_de_resistencia=["Força", "Constituição"],
    ferramentas=[],
    quantidade_de_pericias=2,
    pericias=["Adestrar Animais", "Atletismo" "Intimidação" "Natureza" "Percepção", "Sobrevivência"])

Bardo = Classes(dado_de_vida="1d8",
    armas=["Armas simples", "Bestas de Mão", "Espadas curtas", "Espadas longas", "Ra"], 
    armaduras=["Armadura leve"],
    testes_de_resistencia=["Destreza", "Carisma"],
    ferramentas=["Três instrumentos musicais, à sua escolha"],#pode ser uma herança
    quantidade_de_pericias=3)

