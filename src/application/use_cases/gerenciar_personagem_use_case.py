from typing import List, Optional

from src.infrastructure.repositories.personagem_repository import IPersonagemRepository
from src.domain.models.personagem import Personagem
from src.infrastructure.repositories.raca_repository import IRacaRepository
from src.infrastructure.repositories.classe_repository import IClasseRepository
from src.infrastructure.repositories.habilidades_raciais_repository import IHabilidadesRaciaisRepository
from src.infrastructure.repositories.spell_repository import ISpellRepository

class GerenciarPersonagemUseCase:
    def __init__(
        self,
        personagem_repository: IPersonagemRepository,
        raca_repository: IRacaRepository,
        classe_repository: IClasseRepository,
        habilidades_raciais_repository: IHabilidadesRaciaisRepository,
        spell_repository: ISpellRepository
    ):
        self._personagem_repository = personagem_repository
        self._raca_repository = raca_repository
        self._classe_repository = classe_repository
        self._habilidades_raciais_repository = habilidades_raciais_repository
        self._spell_repository = spell_repository

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

    # Futuros métodos que podem usar self._spell_repository, por exemplo:
    # def get_magias_conhecidas_personagem(self, personagem: Personagem) -> List[Dict[str, Any]]:
    #     # Lógica para determinar magias conhecidas baseadas na classe, nível, etc.
    #     return self._spell_repository.get_spells_by_class(personagem.classe_nome)