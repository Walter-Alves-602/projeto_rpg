from dataclasses import dataclass

@dataclass
class Classes:
    dado_de_vida: str
    armas: list
    armaduras: list
    testes_de_resistencia: list
    ferramentas: list
    quantidade_de_pericias: int
    # Removemos a referência direta a pericias.keys() aqui.
    # As pericias serão passadas durante a criação da instância ou gerenciadas por um serviço.
    pericias_disponiveis: list # Adicionamos este campo para listar as perícias que a classe pode escolher.

