from typing import List, Optional

from src.domain.ports import IPersonagemRepository, IRacaRepository, IClasseRepository, IHabilidadesRaciaisRepository, ISpellRepository
from src.domain.models.personagem import Personagem
from src.domain.services import DiceRoller

class GerenciarPersonagemUseCase:
    def __init__(
        self,
        personagem_repository: IPersonagemRepository,
        raca_repository: IRacaRepository,
        classe_repository: IClasseRepository,
        habilidades_raciais_repository: IHabilidadesRaciaisRepository,
        spell_repository: ISpellRepository
    ):
        self._personagem_repository: IPersonagemRepository = personagem_repository
        self._raca_repository: IRacaRepository = raca_repository
        self._classe_repository: IClasseRepository = classe_repository
        self._habilidades_raciais_repository: IHabilidadesRaciaisRepository = habilidades_raciais_repository
        self._spell_repository: ISpellRepository = spell_repository

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
            raca_repository=self._raca_repository,
            classe_repository=self._classe_repository
        )
        # Salva o novo personagem através do repositório de personagens.
        self._personagem_repository.save(novo_personagem)
        return novo_personagem

    def obter_personagem_por_nome(self, nome: str) -> Optional[Personagem]:
        return self._personagem_repository.get_by_name(nome)

    def listar_todos_personagens(self) -> List[Personagem]:
        return self._personagem_repository.get_all()

    def excluir_personagem(self, nome: str) -> None:
        personagem = self._personagem_repository.get_by_name(nome)
        if not personagem:
            raise ValueError(f"Personagem '{nome}' não encontrado para exclusão.")
        self._personagem_repository.delete(nome)