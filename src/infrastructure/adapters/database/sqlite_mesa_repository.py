from typing import List, Optional

from src.domain.models import Mesa
from src.domain.ports import MesaRepositoryPort
from src.persistence import DatabaseManager


class SQLiteMesaRepository(MesaRepositoryPort):
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def salvar(self, mesa: Mesa) -> None:
        # Salva a mesa principal
        query_mesa = "INSERT OR REPLACE INTO mesas (id, nome, descricao) VALUES (?, ?, ?)"
        self.db_manager.execute_query(query_mesa, (mesa.id, mesa.nome, mesa.descricao))

        # Limpa associações de usuários antigas para esta mesa
        delete_query = "DELETE FROM mesas_usuarios WHERE mesa_id = ?"
        self.db_manager.execute_query(delete_query, (mesa.id,))

        # Insere os mestres com o papel correto
        for mestre_id in mesa.mestres:
            self.adicionar_mestre(mesa.id, mestre_id)

        # Insere os jogadores com o papel correto
        for jogador_id in mesa.jogadores:
            self.adicionar_jogador(mesa.id, jogador_id)

        # Limpa e insere personagens na tabela de associação (aqui a função genérica ainda serve)
        self._atualizar_associacao("mesas_personagens", "personagem_id", mesa.id, mesa.personagens)

    def buscar_por_id(self, mesa_id: str) -> Optional[Mesa]:
        query = "SELECT * FROM mesas WHERE id = ?"
        row = self.db_manager.fetch_one(query, (mesa_id,))
        if not row:
            return None

        # Usando o construtor do Pydantic diretamente, pois from_orm pode estar depreciado
        mesa = Mesa(id=row["id"], nome=row["nome"], descricao=row["descricao"])
        mesa.mestres = self._buscar_associacao("mesas_usuarios", "usuario_id", mesa_id, papel="mestre")
        mesa.jogadores = self._buscar_associacao("mesas_usuarios", "usuario_id", mesa_id, papel="jogador")
        mesa.personagens = self._buscar_associacao("mesas_personagens", "personagem_id", mesa_id)
        return mesa

    def listar_por_usuario_id(self, usuario_id: str) -> List[Mesa]:
        query = """
            SELECT DISTINCT m.id FROM mesas m
            JOIN mesas_usuarios mu ON m.id = mu.mesa_id
            WHERE mu.usuario_id = ?
        """
        rows = self.db_manager.fetch_all(query, (usuario_id,))
        # O fetch_all retorna uma lista de dicionários
        mesa_ids = [row["id"] for row in rows]
        return [self.buscar_por_id(mesa_id) for mesa_id in mesa_ids if self.buscar_por_id(mesa_id) is not None]

    def adicionar_jogador(self, mesa_id: str, usuario_id: str) -> None:
        query = "INSERT OR IGNORE INTO mesas_usuarios (mesa_id, usuario_id, papel) VALUES (?, ?, ?)"
        self.db_manager.execute_query(query, (mesa_id, usuario_id, "jogador"))

    def remover_jogador(self, mesa_id: str, usuario_id: str) -> None:
        query = "DELETE FROM mesas_usuarios WHERE mesa_id = ? AND usuario_id = ?"
        self.db_manager.execute_query(query, (mesa_id, usuario_id))

    def adicionar_mestre(self, mesa_id: str, usuario_id: str) -> None:
        query = "INSERT OR IGNORE INTO mesas_usuarios (mesa_id, usuario_id, papel) VALUES (?, ?, ?)"
        self.db_manager.execute_query(query, (mesa_id, usuario_id, "mestre"))

    def adicionar_personagem(self, mesa_id: str, personagem_id: str) -> None:
        query = "INSERT OR IGNORE INTO mesas_personagens (mesa_id, personagem_id) VALUES (?, ?)"
        self.db_manager.execute_query(query, (mesa_id, personagem_id))

    def remover_personagem(self, mesa_id: str, personagem_id: str) -> None:
        query = "DELETE FROM mesas_personagens WHERE mesa_id = ? AND personagem_id = ?"
        self.db_manager.execute_query(query, (mesa_id, personagem_id))

    def _atualizar_associacao(self, tabela: str, coluna_id: str, mesa_id: str, ids: List[str]):
        # Limpa associações antigas
        delete_query = f"DELETE FROM {tabela} WHERE mesa_id = ?"
        self.db_manager.execute_query(delete_query, (mesa_id,))
        # Insere novas associações
        for item_id in ids:
            insert_query = f"INSERT INTO {tabela} (mesa_id, {coluna_id}) VALUES (?, ?)"
            self.db_manager.execute_query(insert_query, (mesa_id, item_id))

    def _buscar_associacao(self, tabela: str, coluna_id: str, mesa_id: str, papel: Optional[str] = None) -> List[str]:
        query = f"SELECT {coluna_id} FROM {tabela} WHERE mesa_id = ?"
        params = [mesa_id]
        if papel:
            query += " AND papel = ?"
            params.append(papel)

        rows = self.db_manager.fetch_all(query, tuple(params))
        return [row[coluna_id] for row in rows]
