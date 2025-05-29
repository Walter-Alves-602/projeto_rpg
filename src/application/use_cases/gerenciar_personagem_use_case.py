# src/application/use_cases/gerenciar_personagem_use_case.py

from typing import List, Optional

from src.infrastructure.repositories.personagem_repository import IPersonagemRepository
from src.domain.models.personagem import Personagem

# --- NOVIDADE AQUI: Importa as interfaces dos repositórios adicionais ---
from src.infrastructure.repositories.raca_repository import IRacaRepository
from src.infrastructure.repositories.classe_repository import IClasseRepository
from src.infrastructure.repositories.habilidades_raciais_repository import (
    IHabilidadesRaciaisRepository,
)

# --- FIM NOVIDADE ---


class GerenciarPersonagemUseCase:
    def __init__(
        self,
        personagem_repository: IPersonagemRepository,
        # --- NOVIDADE AQUI: Novos parâmetros no construtor ---
        raca_repository: IRacaRepository,
        classe_repository: IClasseRepository,
        habilidades_raciais_repository: IHabilidadesRaciaisRepository,
        # --- FIM NOVIDADE ---
    ):
        self._personagem_repository = personagem_repository
        # --- NOVIDADE AQUI: Armazena os novos repositórios ---
        self._raca_repository = raca_repository
        self._classe_repository = classe_repository
        self._habilidades_raciais_repository = habilidades_raciais_repository
        # --- FIM NOVIDADE ---

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
        # Quando criamos um personagem, precisamos passar os repositórios para o construtor de Personagem
        # agora que ele não recebe mais o habilidades_raciais_repository no init do Personagem.
        # No entanto, a classe Personagem em si ainda precisa do raca_repository e classe_repository.
        # E ela NÃO precisa do habilidades_raciais_repository no seu __init__ (lembra da sua otimização?).
        # O self.habilidades_raciais_nomes é preenchido diretamente do dado da raça.

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
            raca_repository=self._raca_repository,  # Passa o raca_repository aqui
            classe_repository=self._classe_repository,  # Passa o classe_repository aqui
            # --- REMOVIDO: habilidades_raciais_repository NÃO é mais passado para o construtor do Personagem
            # pois ele é usado apenas no método get_habilidades_raciais_com_descricao() ---
            # habilidades_raciais_repository=self._habilidades_raciais_repository
            # --- FIM REMOVIDO ---
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
