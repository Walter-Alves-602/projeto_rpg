# src/domain/models/personagem.py
import src.domain.models.armas as armas # Importa o módulo armas da nova localização
from src.infrastructure.repositories.raca_repository import IRacaRepository
from src.infrastructure.repositories.classe_repository import IClasseRepository
from src.domain.models.classes import Classes # Importa a classe Classes da nova localização

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
        raca_repository: IRacaRepository, # Injetamos o repositório de raças
        classe_repository: IClasseRepository # Injetamos o repositório de classes
    ):
        self.nome = nome
        self.jogador = jogador
        self.nivel = nivel

        # Repositórios injetados para buscar dados
        self._raca_repository = raca_repository
        self._classe_repository = classe_repository

        # Carregar dados da raça e classe
        self.raca = self._raca_repository.get_raca(raca_nome)
        self.classe = self._classe_repository.get_classe(classe_nome)

        if not self.raca:
            raise ValueError(f"Raça '{raca_nome}' não encontrada.")
        if not self.classe:
            raise ValueError(f"Classe '{classe_nome}' não encontrada.")

        self.atributos = {
            "forca": forca,
            "destreza": destreza,
            "constituicao": constituicao,
            "inteligencia": inteligencia,
            "sabedoria": sabedoria,
            "carisma": carisma,
        }

        # Aplicando os modificadores de raça
        self._aplicar_modificadores_raca()

        # Calculando modificadores de atributo
        self.modificadores_atributo = {attr: ((value - 10) // 2) for attr, value in self.atributos.items()}

        # Inicializando HP (a lógica completa virá depois)
        self.pontos_de_vida_max = 0
        self.pontos_de_vida_atual = 0
        self.pontos_de_experiencia = 0

        self.inventario = []
        self.linguas = self.raca.get("linguas", []) # As línguas vêm diretamente dos dados da raça

        # Atributos da classe (proficiências, etc.)
        self.proficiencias_armas = self.classe.get("armas", [])
        self.proficiencias_armaduras = self.classe.get("armaduras", [])
        self.testes_de_resistencia = self.classe.get("testes_de_resistencia", [])
        self.ferramentas = self.classe.get("ferramentas", [])
        self.quantidade_de_pericias_classe = self.classe.get("quantidade_de_pericias", 0)
        self.pericias_disponiveis_para_escolha = self._classe_repository.get_pericias_por_classe(classe_nome)
        self.pericias_escolhidas = [] # O usuário escolherá as perícias posteriormente
        self.raca_nome = raca_nome
        self.classe_nome = classe_nome

    def _aplicar_modificadores_raca(self):
        """
        Aplica os modificadores de atributo da raça aos atributos base do personagem.
        """
        modificadores = self.raca.get("atributos", {})
        for atributo, valor_modificador in modificadores.items():
            self.atributos[atributo] += valor_modificador

    # Métodos de inventário
    def adicionar_item_inventario(self, item):
        self.inventario.append(item)

    def remover_item_inventario(self, item):
        if item in self.inventario:
            self.inventario.remove(item)
        else:
            print(f"Item {item} não encontrado no inventário.")