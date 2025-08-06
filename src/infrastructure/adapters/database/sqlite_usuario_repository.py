from typing import Optional

from src.domain.models.usuario import PapelUsuario, Usuario
from src.domain.ports.usuario_repository import UsuarioRepositoryPort
from src.persistence.database_manager import DatabaseManager


class SQLiteUsuarioRepository(UsuarioRepositoryPort):
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def salvar(self, usuario: Usuario) -> None:
        query = "INSERT OR REPLACE INTO usuarios (id, username, hashed_password, papel) VALUES (?, ?, ?, ?)"
        params = (usuario.id, usuario.username, usuario.hashed_password, usuario.papel.value)
        self.db_manager.execute_query(query, params)

    def buscar_por_username(self, username: str) -> Optional[Usuario]:
        query = "SELECT id, username, hashed_password, papel FROM usuarios WHERE username = ?"
        row = self.db_manager.fetch_one(query, (username,))
        if row:
            return Usuario(
                id=row["id"],
                username=row["username"],
                hashed_password=row["hashed_password"],
                papel=PapelUsuario(row["papel"])
            )
        return None

    def buscar_por_id(self, usuario_id: str) -> Optional[Usuario]:
        query = "SELECT id, username, hashed_password, papel FROM usuarios WHERE id = ?"
        row = self.db_manager.fetch_one(query, (usuario_id,))
        if row:
            return Usuario(
                id=row["id"],
                username=row["username"],
                hashed_password=row["hashed_password"],
                papel=PapelUsuario(row["papel"])
            )
        return None

    def buscar_por_mesa(self, mesa_id: str) -> Optional[Usuario]:
        query = "SELECT id, username, papel FROM usuarios WHERE mesa_id = ?"
        row = self.db_manager.fetch_one(query, (mesa_id,))
        if row:
            return Usuario(
                id=row["id"],
                username=row["username"],
                hashed_password=row["hashed_password"],
                papel=PapelUsuario(row["papel"])
            )
        return None