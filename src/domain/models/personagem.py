from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.domain.ports import IRacaRepository, IClasseRepository

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
        raca_repository: "IRacaRepository",
        classe_repository: "IClasseRepository",
    ):
        self.nome = nome
        self.jogador = jogador
        self.nivel = nivel
        self.raca_nome = raca_nome
        self.classe_nome = classe_nome
        self._raca_repository = raca_repository
        self._classe_repository = classe_repository
        self.raca = self._raca_repository.get_raca(self.raca_nome)
        self.classe = self._classe_repository.get_classe(self.classe_nome)

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
        self.pericias_disponiveis_para_escolha = self._classe_repository.get_pericias_por_classe(self.classe_nome)
        self.pericias_escolhidas = []

        self.habilidades_raciais_nomes: list[str] = self.raca.get("habilidades_raciais", [])
        self.habilidades_extras: list[str] = []

    def _aplicar_modificadores_raca(self):
        modificadores = self.raca.get("atributos", {})
        for atributo, valor_modificador in modificadores.items():
            self.atributos[atributo] += valor_modificador

    def adicionar_item_inventario(self, item):
        self.inventario.append(item)

    def remover_item_inventario(self, item):
        if item in self.inventario:
            self.inventario.remove(item)
        else:
            print(f"Item {item} não encontrado no inventário.")

    def get_habilidades_raciais_com_descricao(self, habilidades_raciais_repository: 'IHabilidadesRaciaisRepository') -> list[dict[str, str]]: # pyright: ignore[reportUndefinedVariable]  # noqa: F821
        """
        Retorna uma lista de dicionários, onde cada dicionário contém o nome
        e a descrição de uma habilidade racial do personagem.
        Recebe o repositório de habilidades como parâmetro para buscar as descrições.
        """
        habilidades_detalhadas = []
        for habilidade_nome in self.habilidades_raciais_nomes:
            descricao = habilidades_raciais_repository.get_habilidade_descricao(habilidade_nome)
            if descricao:
                habilidades_detalhadas.append({
                    "nome": habilidade_nome,
                    "descricao": descricao
                })
            else:
                print(f"Aviso: Descrição para a habilidade '{habilidade_nome}' não encontrada no repositório de habilidades.")
        return habilidades_detalhadas

    def update_habilidade_extra():
        pass