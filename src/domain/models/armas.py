class Arma:
    def __init__(
        self, nome, custo, dano, tipo_dano, peso, propriedades=None, marcial=False
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
        self, nome, custo, dano, tipo_dano, peso, propriedades=None, marcial=False
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
        alcance,
        municao=None,
        propriedades=None,
        marcial=False,
    ):
        super().__init__(nome, custo, dano, tipo_dano, peso, propriedades, marcial)
        self.alcance = alcance
        self.municao = municao


Adaga = ArmaCorpoACorpo(
    "Adaga", "2 PO", "1d4", "Perfurante", 0.5, ["Leve", "Arremesso (6/18)"]
)
EspadaCurta = ArmaCorpoACorpo(
    "Espada Curta", "10 PO", "1d6", "Perfurante", 1, ["Leve", "Finesse"], True
)
ArcoLongo = ArmaDeAtaqueDistancia(
    "Arco Longo",
    "50 PO",
    "1d8",
    "Perfurante",
    1,
    "45/180",
    "Flechas",
    ["Duas Mãos", "Munição"],
    True,
)
BestaLeve = ArmaDeAtaqueDistancia(
    "Besta Leve",
    "25 PO",
    "1d8",
    "Perfurante",
    2.5,
    "24/96",
    "Virotes",
    ["Recarga", "Duas Mãos", "Munição"],
    True,
)

LISTA_DE_ARMAS = [Adaga, EspadaCurta, ArcoLongo, BestaLeve]
