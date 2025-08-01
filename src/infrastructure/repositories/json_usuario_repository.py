import json
import os
from typing import Dict, Optional

from src.domain.models.usuario import Usuario
from src.domain.ports.usuario_repository import UsuarioRepositoryPort


class JsonUsuarioRepository(UsuarioRepositoryPort):
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._dados: Dict[str, dict] = self._carregar_dados()

    def _carregar_dados(self) -> Dict[str, dict]:
        if not os.path.exists(self._db_path):
            return {}
        with open(self._db_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def _salvar_dados(self):
        with open(self._db_path, "w", encoding="utf-8") as f:
            json.dump(self._dados, f, indent=4, ensure_ascii=False)

    def salvar(self, usuario: Usuario) -> None:
        # Usamos o username como chave principal no nosso "banco" JSON
        self._dados[usuario.username] = usuario.model_dump()
        self._salvar_dados()

    def buscar_por_username(self, username: str) -> Optional[Usuario]:
        dados_usuario = self._dados.get(username)
        if dados_usuario:
            return Usuario(**dados_usuario)
        return None