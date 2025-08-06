from typing import List, Optional


class Arma:
    def __init__(
        self, nome: str, custo: str, dano: str, tipo_dano: str, peso: float, propriedades: Optional[List[str]] = None, marcial: bool = False
    ):
        self.nome = nome
        self.custo = custo
        self.dano = dano
        self.tipo_dano = tipo_dano
        self.peso = peso
        self.propriedades = propriedades if propriedades else []
        self.marcial = marcial

    def __str__(self):
        return f"{self.nome} ({self.dano} {self.tipo_dano})"


class ArmaCorpoACorpo(Arma):
    def __init__(
        self, nome: str, custo: str, dano: str, tipo_dano: str, peso: float, propriedades: Optional[List[str]] = None, marcial: bool = False
    ):
        super().__init__(nome, custo, dano, tipo_dano, peso, propriedades, marcial)


class ArmaDeAtaqueDistancia(Arma):
    def __init__(
        self,
        nome,
        custo,
        dano,
        tipo_dano,
        peso,
        alcance: str,
        municao: Optional[str] = None,
        propriedades: Optional[List[str]] = None,
        marcial: bool = False,
    ):
        super().__init__(nome, custo, dano, tipo_dano, peso, propriedades, marcial)
        self.alcance = alcance
        self.municao = municao
