import json
from typing import List, Optional

from src.domain.models.mesa import Mesa
from src.domain.ports.mesa_repository import MesaRepositoryPort
from src.persistence.database_manager import DatabaseManager


class SQLiteMesaRepository(MesaRepositoryPort):
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def salvar(self, mesa: Mesa) -> None:
        # Salva a mesa principal
        query_mesa = "INSERT OR REPLACE INTO mesas (id, nome, descricao) VALUES (?, ?, ?)"
        self.db_manager.execute_query(query_mesa, (mesa.id, mesa.nome, mesa.descricao))

        # Limpa e insere mestres e jogadores na tabela de associação
        self._atualizar_associacao("mesas_usuarios", "usuario_id", mesa.id, mesa.mestres + mesa.jogadores)
        # Limpa e insere personagens na tabela de associação
        self._atualizar_associacao("mesas_personagens", "personagem_id", mesa.id, mesa.personagens)

    def buscar_por_id(self, mesa_id: str) -> Optional[Mesa]:
        query = "SELECT * FROM mesas WHERE id = ?"
        row = self.db_manager.fetch_one(query, (mesa_id,))
        if not row:
            return None

        mesa = Mesa.from_orm(row)
        mesa.mestres = self._buscar_associacao("mesas_usuarios", "usuario_id", mesa_id, papel="mestre")
        mesa.jogadores = self._buscar_associacao("mesas_usuarios", "usuario_id", mesa_id, papel="jogador")
        mesa.personagens = self._buscar_associacao("mesas_personagens", "personagem_id", mesa_id)
        return mesa

    def listar_por_usuario_id(self, usuario_id: str) -> List[Mesa]:
        query = """
            SELECT m.id FROM mesas m
            JOIN mesas_usuarios mu ON m.id = mu.mesa_id
            WHERE mu.usuario_id = ?
        """
        rows = self.db_manager.fetch_all(query, (usuario_id,))
        return [self.buscar_por_id(row["id"]) for row in rows]

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
