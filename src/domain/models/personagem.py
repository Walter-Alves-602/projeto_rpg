
class Personagem:
    def __init__(
        self,
        nome: str,
        jogador: str,
        raca_nome: str,
        classe_nome: str,
        nivel: int,
        forca: int,
        destreza: int,
        constituicao: int,
        inteligencia: int,
        sabedoria: int,
        carisma: int,
        raca: dict,
        classe: dict,
        pericias_disponiveis: list[str]
    ):
        self.nome = nome
        self.jogador = jogador
        self.nivel = nivel
        self.raca_nome = raca_nome
        self.classe_nome = classe_nome
        self.raca = raca
        self.classe = classe

        if not self.raca:
            raise ValueError(f"Raça '{self.raca_nome}' não encontrada.")
        if not self.classe:
            raise ValueError(f"Classe '{self.classe_nome}' não encontrada.")

        self.atributos = {
            "forca": forca,
            "destreza": destreza,
            "constituicao": constituicao,
            "inteligencia": inteligencia,
            "sabedoria": sabedoria,
            "carisma": carisma,
        }

        self._aplicar_modificadores_raca()
        self.modificadores_atributo = {attr: ((value - 10) // 2) for attr, value in self.atributos.items()}

        self.pontos_de_vida_max = 0
        self.pontos_de_vida_atual = 0
        self.pontos_de_experiencia = 0

        self.inventario = []
        self.linguas = self.raca.get("linguas", [])
        self.deslocamento = self.raca.get("deslocamento", 0)
        self.proficiencias_armas = self.classe.get("armas", [])
        self.proficiencias_armaduras = self.classe.get("armaduras", [])
        self.testes_de_resistencia = self.classe.get("testes_de_resistencia", [])
        self.ferramentas = self.classe.get("ferramentas", [])
        self.quantidade_de_pericias_classe = self.classe.get("quantidade_de_pericias", 0)
        self.pericias_disponiveis_para_escolha = pericias_disponiveis
        self.pericias_escolhidas = []

        self.habilidades_raciais_nomes: list[str] = self.raca.get("habilidades_raciais", [])
        self.habilidades_extras = []

    def _aplicar_modificadores_raca(self):
        modificadores = self.raca.get("atributos", {})
        for atributo, valor_modificador in modificadores.items():
            self.atributos[atributo] += valor_modificador
