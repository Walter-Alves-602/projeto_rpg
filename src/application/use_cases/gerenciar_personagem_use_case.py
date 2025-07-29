from typing import List, Optional

from src.domain.ports import IPersonagemRepository, IRacaRepository, IClasseRepository, IHabilidadesRaciaisRepository, ISpellRepository, IArmaRepository
from src.domain.models.personagem import Personagem
from src.domain.services import DiceRoller

class GerenciarPersonagemUseCase:
    def __init__(
        self,
        personagem_repository: IPersonagemRepository,
        raca_repository: IRacaRepository,
        classe_repository: IClasseRepository,
        habilidades_raciais_repository: IHabilidadesRaciaisRepository,
        spell_repository: ISpellRepository,
        arma_repository: IArmaRepository,
    ):
        self._personagem_repository: IPersonagemRepository = personagem_repository
        self._raca_repository: IRacaRepository = raca_repository
        self._classe_repository: IClasseRepository = classe_repository
        self._habilidades_raciais_repository: IHabilidadesRaciaisRepository = habilidades_raciais_repository
        self._spell_repository: ISpellRepository = spell_repository
        self._arma_repository: IArmaRepository = arma_repository

    def perform_attribute_check(self, personagem_id: int, attribute: str):
        personagem = self._personagem_repository.get_by_id(personagem_id)
        if not personagem:
            raise ValueError("Personagem não encontrado.")

        modifier = personagem.modificadores_atributo[attribute]
        return DiceRoller.roll(20, 1, modifier)

    def criar_personagem(
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
    ) -> Personagem:
        """
        Cria um novo personagem e o salva no repositório.

        Args:
            nome (str): O nome do personagem.
            jogador (str): O nome do jogador que controla o personagem.
            raca_nome (str): O nome da raça do personagem.
            classe_nome (str): O nome da classe do personagem.
            nivel (int): O nível inicial do personagem.
            forca (int): Valor do atributo Força.
            destreza (int): Valor do atributo Destreza.
            constituicao (int): Valor do atributo Constituição.
            inteligencia (int): Valor do atributo Inteligência.
            sabedoria (int): Valor do atributo Sabedoria.
            carisma (int): Valor do atributo Carisma.

        Returns:
            Personagem: O objeto Personagem recém-criado e salvo.
        """
        # O UseCase agora é a "fábrica" que busca as dependências
        raca = self._raca_repository.get_raca(raca_nome)
        if not raca:
            raise ValueError(f"Raça '{raca_nome}' não encontrada.")

        classe = self._classe_repository.get_classe(classe_nome)
        if not classe:
            raise ValueError(f"Classe '{classe_nome}' não encontrada.")

        pericias_disponiveis = self._classe_repository.get_pericias_por_classe(classe_nome)

        # O modelo Personagem recebe os dados já resolvidos
        novo_personagem = Personagem(
            nome=nome,
            jogador=jogador,
            raca_nome=raca_nome,
            classe_nome=classe_nome,
            nivel=nivel,
            forca=forca,
            destreza=destreza,
            constituicao=constituicao,
            inteligencia=inteligencia,
            sabedoria=sabedoria,
            carisma=carisma,
            raca=raca,
            classe=classe,
            pericias_disponiveis=pericias_disponiveis
        )

        
        # Salva o novo personagem através do repositório de personagens.
        self._personagem_repository.save(novo_personagem)
        return novo_personagem

    def adicionar_habilidade_extra(self, personagem_nome: str, nome_habilidade: str, descricao_habilidade: str) -> Optional[Personagem]:
        """
        Adiciona uma habilidade extra a um personagem existente e o salva.

        Args:
            personagem_nome (str): O nome do personagem a ser modificado.
            nome_habilidade (str): O nome da nova habilidade.
            descricao_habilidade (str): A descrição da nova habilidade.

        Returns:
            Personagem: O objeto Personagem atualizado.
        """
        personagem = self._personagem_repository.get_by_name(personagem_nome)
        if not personagem:
            raise ValueError(f"Personagem '{personagem_nome}' não encontrado.")

        personagem.habilidades_extras.append({"nome": nome_habilidade, "descricao": descricao_habilidade})
        self._personagem_repository.save(personagem)
        return personagem

    def obter_habilidades_com_descricao(self, personagem_nome: str) -> list[dict[str, str]]:
        """
        Busca um personagem e retorna uma lista combinada de suas habilidades
        raciais e extras, cada uma com sua descrição.
        """
        personagem = self._personagem_repository.get_by_name(personagem_nome)
        if not personagem:
            return []

        habilidades_detalhadas = []
        # Habilidades Raciais
        for habilidade_nome in personagem.habilidades_raciais_nomes:
            descricao = self._habilidades_raciais_repository.get_habilidade_descricao(habilidade_nome)
            if descricao:
                habilidades_detalhadas.append({"nome": habilidade_nome, "descricao": descricao})

        # Habilidades Extras
        habilidades_detalhadas.extend(personagem.habilidades_extras)

        return habilidades_detalhadas

    def adicionar_item_ao_inventario(self, personagem_nome: str, nome_item: str) -> Optional[Personagem]:
        """
        Adiciona um item (arma) ao inventário de um personagem.
        """
        personagem = self._personagem_repository.get_by_name(personagem_nome)
        if not personagem:
            raise ValueError(f"Personagem '{personagem_nome}' não encontrado.")

        item = self._arma_repository.get_by_name(nome_item)
        if not item:
            raise ValueError(f"Item '{nome_item}' não encontrado no repositório de armas.")

        # A lógica de adicionar acontece aqui, no UseCase
        personagem.inventario.append(item)
        self._personagem_repository.save(personagem)
        return personagem

    def remover_item_do_inventario(self, personagem_nome: str, nome_item: str) -> Optional[Personagem]:
        """
        Remove um item (arma) do inventário de um personagem.
        """
        personagem = self._personagem_repository.get_by_name(personagem_nome)
        if not personagem:
            raise ValueError(f"Personagem '{personagem_nome}' não encontrado.")

        # A lógica de remover acontece aqui, no UseCase
        item_para_remover = next((item for item in personagem.inventario if item.nome == nome_item), None)
        if item_para_remover:
            personagem.inventario.remove(item_para_remover)
            self._personagem_repository.save(personagem)
        return personagem

    def obter_personagem_por_nome(self, nome: str) -> Optional[Personagem]:
        return self._personagem_repository.get_by_name(nome)

    def listar_todos_personagens(self) -> List[Personagem]:
        return self._personagem_repository.get_all()

    def excluir_personagem(self, nome: str) -> None:
        personagem = self._personagem_repository.get_by_name(nome)
        if not personagem:
            raise ValueError(f"Personagem '{nome}' não encontrado para exclusão.")
        self._personagem_repository.delete(nome)