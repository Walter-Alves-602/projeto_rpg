from src.domain.models.usuario import PapelUsuario
from src.domain.services.autenticacao_service import AutenticacaoService
from src.infrastructure.repositories.json_usuario_repository import (
    JsonUsuarioRepository,
)
from src.ui.flet_app import start_flet_app


def main():
    """Ponto de entrada principal e Composition Root da aplicação."""

    # 1. Instanciar o Adaptador de Repositório (a implementação concreta)
    usuario_repo = JsonUsuarioRepository(db_path="usuarios.json")

    # 2. Instanciar o Serviço de Domínio, injetando o adaptador como dependência
    auth_service = AutenticacaoService(usuario_repo=usuario_repo)

    # 3. Iniciar a aplicação de UI, passando o serviço de autenticação para ela.
    # A UI agora tem acesso à lógica de negócio sem saber dos detalhes de implementação.
    start_flet_app(auth_service)


if __name__ == "__main__":
    main()
