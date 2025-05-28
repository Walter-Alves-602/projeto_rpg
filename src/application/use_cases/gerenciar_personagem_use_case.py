# src/application/use_cases/gerenciar_personagem_use_case.py
from typing import List, Optional
from src.domain.models.personagem import Personagem
from src.infrastructure.repositories.personagem_repository import IPersonagemRepository

class GerenciarPersonagemUseCase:
    def __init__(self, personagem_repository: IPersonagemRepository):
        self._personagem_repository = personagem_repository

    def salvar_personagem(self, personagem: Personagem) -> None:
        """
        Salva um personagem existente ou um novo personagem.
        """
        self._personagem_repository.save(personagem)
        print(f"Personagem '{personagem.nome}' salvo com sucesso!")

    def carregar_personagem(self, nome: str) -> Optional[Personagem]:
        """
        Carrega um personagem pelo nome.
        """
        personagem = self._personagem_repository.get_by_name(nome)
        if personagem:
            print(f"Personagem '{personagem.nome}' carregado com sucesso.")
        else:
            print(f"Personagem '{nome}' não encontrado.")
        return personagem

    def listar_todos_personagens(self) -> List[Personagem]:
        """
        Lista todos os personagens salvos.
        """
        personagens = self._personagem_repository.get_all()
        if personagens:
            print("Personagens salvos:")
            for p in personagens:
                print(f"- {p.nome} (Raça: {p.raca.get('nome', p.raca_nome)}, Classe: {p.classe.get('nome', p.classe_nome)})")
        else:
            print("Nenhum personagem salvo ainda.")
        return personagens

    def deletar_personagem(self, nome: str) -> None:
        """
        Deleta um personagem pelo nome.
        """
        self._personagem_repository.delete(nome)
        print(f"Personagem '{nome}' deletado (se existia).")