import bcrypt
from typing import Optional

from src.domain.models.usuario import Usuario, PapelUsuario
from src.domain.ports.usuario_repository import UsuarioRepositoryPort

class AutenticacaoService:
    def __init__(self, usuario_repo: UsuarioRepositoryPort):
        self._usuario_repo = usuario_repo

    def registrar_usuario(self, username: str, password: str, papel: PapelUsuario) -> Usuario:
        if self._usuario_repo.buscar_por_username(username):
            raise ValueError("Nome de usuário já existe.")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        novo_usuario = Usuario(username=username, hashed_password=hashed_password, papel=papel)
        self._usuario_repo.salvar(novo_usuario)
        return novo_usuario

    def autenticar_usuario(self, username: str, password: str) -> Optional[Usuario]:
        usuario = self._usuario_repo.buscar_por_username(username)
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario.hashed_password.encode('utf-8')):
            return usuario
        return None

