from typing import List, Optional

from src.domain.ports.personagem_repository import PersonagemRepositoryPort
from src.domain.ports.raca_repository import RacaRepositoryPort
from src.domain.ports.classe_repository import ClasseRepositoryPort
from src.domain.models.personagem import Personagem
from src.domain.services.dice_roller import DiceRoller


class GerenciarPersonagemUseCase:
    def __init__(
        self,
        personagem_repository: PersonagemRepositoryPort,
        raca_repository: RacaRepositoryPort,
        classe_repository: ClasseRepositoryPort,
    ):
        self.personagem_repository = personagem_repository
        self.raca_repository = raca_repository
        self.classe_repository = classe_repository

    def criar_personagem(self, dados_personagem: dict) -> Personagem:
        """Cria um novo personagem com base nos dados fornecidos."""
        raca = self.raca_repository.get_raca(dados_personagem["raca_nome"])
        classe = self.classe_repository.get_classe(dados_personagem["classe_nome"])

        if not raca or not classe:
            raise ValueError("Raça ou Classe não encontrada.")

        # Lógica para calcular PV, deslocamento, etc.
        constituicao = dados_personagem.get("constituicao", 10)
        mod_constituicao = (constituicao - 10) // 2
        pontos_de_vida_max = DiceRoller.get_max_value(classe.get("dado_de_vida", "1d8") )+ mod_constituicao

        # Cria o objeto Personagem usando Pydantic
        novo_personagem = Personagem(
            **dados_personagem,
            pontos_de_vida_max=pontos_de_vida_max,
            pontos_de_vida_atual=pontos_de_vida_max,
            deslocamento=float(raca.get("deslocamento", 9.0)),
            linguas=raca.get("linguas", []),
            proficiencias_armas=classe.get("armas", []),
            proficiencias_armaduras=classe.get("armaduras", []),
            testes_de_resistencia=classe.get("testes_de_resistencia", []),
            habilidades_raciais=raca.get("habilidades_raciais", [])
        )

        self.personagem_repository.salvar(novo_personagem)
        return novo_personagem

    def listar_personagens_por_jogador(self, jogador_id: str) -> List[Personagem]:
        """Lista todos os personagens pertencentes a um jogador específico."""
        todos_personagens = self.personagem_repository.listar_todos()
        return [p for p in todos_personagens if p.jogador == jogador_id]

    def buscar_personagem_por_id(self, personagem_id: str) -> Optional[Personagem]:
        return self.personagem_repository.buscar_por_id(personagem_id)

    def deletar_personagem(self, personagem_id: str) -> None:
        self.personagem_repository.deletar(personagem_id)
