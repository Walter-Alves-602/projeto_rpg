from typing import List

from src.domain.models.mesa import Mesa
from src.domain.models.personagem import Personagem
from src.domain.models.usuario import Usuario, PapelUsuario
from src.domain.ports.mesa_repository import MesaRepositoryPort
from src.domain.ports.usuario_repository import UsuarioRepositoryPort
from src.domain.ports.personagem_repository import PersonagemRepositoryPort

class GerenciarMesaUseCase:
    def __init__(
        self,
        mesa_repository: MesaRepositoryPort,
        usuario_repository: UsuarioRepositoryPort,
        personagem_repository: PersonagemRepositoryPort
    ):
        self.mesa_repository = mesa_repository
        self.usuario_repository = usuario_repository
        self.personagem_repository = personagem_repository

    def criar_mesa(self, nome: str, descricao: str, mestre_id: str) -> Mesa:
        """Cria uma nova mesa e define o criador como o primeiro mestre."""
        mestre = self.usuario_repository.buscar_por_id(mestre_id)
        if not mestre or mestre.papel != PapelUsuario.MESTRE:
            raise ValueError("Apenas usuários com o papel de 'mestre' podem criar mesas.")

        nova_mesa = Mesa(nome=nome, descricao=descricao, mestres=[mestre_id])
        self.mesa_repository.salvar(nova_mesa)
        return nova_mesa

    def adicionar_usuario(self, mesa_id: str, username_adicionar: str, mestre_id: str, papel: PapelUsuario):
        """Adiciona um usuário (mestre ou jogador) a uma mesa, validando a permissão do mestre."""
        mesa = self.mesa_repository.buscar_por_id(mesa_id)
        if not mesa or mestre_id not in mesa.mestres:
            raise PermissionError("Apenas mestres da mesa podem adicionar novos usuários.")

        usuario_a_adicionar = self.usuario_repository.buscar_por_username(username_adicionar)
        if not usuario_a_adicionar:
            raise ValueError(f'Usuário "{username_adicionar}" não encontrado.')

        if papel == PapelUsuario.JOGADOR:
            self.mesa_repository.adicionar_jogador(mesa_id, usuario_a_adicionar.id)
        elif papel == PapelUsuario.MESTRE:
            self.mesa_repository.adicionar_mestre(mesa_id, usuario_a_adicionar.id)

    def adicionar_personagem_a_mesa(self, mesa_id: str, personagem_id: str, usuario_id: str):
        """Adiciona um personagem a uma mesa, validando se o usuário é o dono."""
        mesa = self.mesa_repository.buscar_por_id(mesa_id)
        personagem = self.personagem_repository.buscar_por_id(personagem_id)

        if not mesa or not personagem:
            raise ValueError("Mesa ou personagem não encontrado.")

        if usuario_id not in mesa.jogadores and usuario_id not in mesa.mestres:
            raise PermissionError("Usuário não faz parte desta mesa.")

        if personagem.jogador != usuario_id:
            raise PermissionError("Você não é o dono deste personagem.")

        self.mesa_repository.adicionar_personagem(mesa_id, personagem.id)

    def listar_mesas_do_usuario(self, usuario_id: str) -> List[Mesa]:
        """Retorna todas as mesas associadas a um usuário."""
        return self.mesa_repository.listar_por_usuario_id(usuario_id)

    def listar_personagens_da_mesa(self, mesa_id: str, usuario_id: str) -> List[Personagem]:
        """Retorna uma lista de personagens da mesa com base no papel do usuário."""
        mesa = self.mesa_repository.buscar_por_id(mesa_id)
        usuario = self.usuario_repository.buscar_por_id(usuario_id)

        if not mesa or not usuario:
            raise ValueError("Mesa ou usuário não encontrado.")

        if usuario_id not in mesa.mestres and usuario_id not in mesa.jogadores:
            raise PermissionError("Você não tem permissão para ver esta mesa.")

        # Busca todos os personagens da mesa primeiro
        todos_personagens_da_mesa = self.personagem_repository.listar_por_ids(mesa.personagens)

        # Se o usuário for um mestre da mesa, retorna todos
        if usuario.papel == PapelUsuario.MESTRE and usuario_id in mesa.mestres:
            return todos_personagens_da_mesa
        
        # Se for jogador, filtra apenas os seus
        personagens_do_jogador = [p for p in todos_personagens_da_mesa if p.jogador == usuario_id]
        return personagens_do_jogador
