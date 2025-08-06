from typing import List, Optional

from src.domain.models import Personagem
from src.domain.ports import ClasseRepositoryPort, PersonagemRepositoryPort, RacaRepositoryPort, HabilidadesRaciaisRepositoryPort
from src.domain.services import DiceRoller


class GerenciarPersonagemUseCase:
    def __init__(
        self,
        personagem_repository: PersonagemRepositoryPort,
        raca_repository: RacaRepositoryPort,
        classe_repository: ClasseRepositoryPort,
        habilidades_raciais_repository: HabilidadesRaciaisRepositoryPort
    ):
        self.personagem_repository = personagem_repository
        self.raca_repository = raca_repository
        self.classe_repository = classe_repository
        self.habilidades_raciais_repository = habilidades_raciais_repository

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

    def listar_personagens_por_mesa(self, mesa_id: str) -> List[Personagem]:
        return self.personagem_repository.listar_por_mesa(mesa_id)
    
    def obter_habilidades_com_descricao(self, personagem_id: str) -> List[dict]:
        """Obtém todas as habilidades com descrição de um personagem."""
        personagem = self.personagem_repository.buscar_por_id(personagem_id)
        if not personagem:
            return []

        habilidades = []
        for habilidade in personagem.habilidades_raciais + personagem.habilidades_extras:
            descricao = self.habilidades_raciais_repository.get_habilidade_descricao(habilidade)
            habilidades.append({
                "nome": habilidade,
                "descricao": descricao
            })
        return habilidades
    
    def adicionar_habilidade_extra(self, personagem_id: str, nome_habilidade: str, descricao_habilidade: str) -> Personagem:
        """Adiciona uma nova habilidade extra a um personagem."""
        personagem = self.personagem_repository.buscar_por_id(personagem_id)
        if not personagem:
            raise ValueError("Personagem não encontrado.")

        habilidades_extras = []
        for h in personagem.habilidades_extras:
            habilidades_extras.append(h)

        # Verifica se a habilidade já existe
        if any(h['nome'] == nome_habilidade for h in habilidades_extras):
            raise ValueError("Habilidade extra já existe.")
        
        # Adiciona a nova habilidade extra como dicionário
        personagem.habilidades_extras.append({"nome": nome_habilidade, "descricao": descricao_habilidade})

        # Atualiza o repositório
        self.personagem_repository.salvar(personagem)
        return personagem
