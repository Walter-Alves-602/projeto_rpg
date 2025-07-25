# src/application/use_cases/criar_personagem_use_case.py
from src.domain.models.personagem import Personagem
from src.domain.ports import IRacaRepository, IClasseRepository


class CriarPersonagemUseCase:
    def __init__(
        self, raca_repository: IRacaRepository, classe_repository: IClasseRepository
    ):
        self._raca_repository = raca_repository
        self._classe_repository = classe_repository

    def execute(
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
        Cria uma nova instância de Personagem com base nos dados fornecidos,
        utilizando os repositórios para buscar informações de raça e classe.
        """
        personagem = Personagem(
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
            classe_repository=self._classe_repository,
        )
        return personagem
