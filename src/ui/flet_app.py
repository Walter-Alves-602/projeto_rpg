import os
import sys

import flet as ft

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.application.use_cases import GerenciarMesaUseCase, GerenciarPersonagemUseCase
from src.domain.services import AutenticacaoService
from src.infrastructure.adapters.data_files import (
    ArmaFileAdapter,
    ClasseFileAdapter,
    HabilidadesRaciaisFileAdapter,
    RacaFileAdapter,
    SpellFileAdapter,
)
from src.infrastructure.adapters.database import (
    SQLitePersonagemRepository,
    SQLiteUsuarioRepository,
    SQLiteMesaRepository,
)
from src.persistence import DatabaseManager
from src.ui.pages import (
    character_sheet_page,
    create_character_form_page,
    login_page,
    mesa_view_page,
    register_page,
    user_page,
)


class CharacterSheetApp:
    def __init__(self):
        self._init_dependencies()
        self.current_character = None
        self.current_user = None
        self.current_mesa = None
        self.atributo_rodado = None
        self.resultado_teste_atributo = {}

    def set_current_character(self, personagem):
        # Garante que habilidades_extras é uma lista de dicionários
        habilidades_extras = []
        for h in getattr(personagem, "habilidades_extras", []):
            if isinstance(h, dict):
                habilidades_extras.append(h)
            else:
                habilidades_extras.append({"nome": str(h), "descricao": ""})
        personagem.habilidades_extras = habilidades_extras
        self.current_character = personagem

    def _init_dependencies(self):
        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()
        self.raca_repository = RacaFileAdapter()
        self.classe_repository = ClasseFileAdapter()
        self.habilidades_raciais_repository = HabilidadesRaciaisFileAdapter()
        self.spell_repository = SpellFileAdapter()
        self.armas_repository = ArmaFileAdapter()
        self.usuario_repository = SQLiteUsuarioRepository(self.db_manager)
        self.autenticacao_service = AutenticacaoService(self.usuario_repository)
        self.mesa_repository = SQLiteMesaRepository(self.db_manager)
        self.personagem_repository = SQLitePersonagemRepository(self.db_manager)
        self.gerenciar_personagem_uc = GerenciarPersonagemUseCase(
            self.personagem_repository,
            self.raca_repository,
            self.classe_repository,
            self.habilidades_raciais_repository,
        )
        self.gerenciar_mesa_uc = GerenciarMesaUseCase(
            self.mesa_repository, self.usuario_repository, self.personagem_repository
        )

    def registrar_usuario(self, username, password, role):
        return self.autenticacao_service.registrar_usuario(username, password, role)

    def autenticar_usuario(self, username, password):
        user = self.autenticacao_service.autenticar_usuario(username, password)
        if user:
            self.current_user = user
        return user

    def _get_view(self, route, page):
        routes = {
            "/": lambda: login_page(self, page),
            "/register": lambda: register_page(self, page),
            "/create_character": lambda: create_character_form_page(self, page),
            "/user_page": lambda: user_page(self, page),
            "/view_character": lambda: character_sheet_page(self, page),
            "/view_mesa": lambda: mesa_view_page(self, page),
        }
        return routes.get(route, lambda: login_page(self, page))()

    def route_change(self, route):
        page = route.page
        page.views.clear()

        view_content = self._get_view(page.route, page)

        scroll_mode = None
        vertical_alignment = ft.MainAxisAlignment.CENTER

        if page.route == "/view_character":
            scroll_mode = ft.ScrollMode.ADAPTIVE
            vertical_alignment = ft.MainAxisAlignment.START

        page.views.append(
            ft.View(
                page.route,
                [view_content],
                scroll=scroll_mode,
                vertical_alignment=vertical_alignment,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    def _config_page(self, page: ft.Page):
        page.title = "Gerenciador de Personagens D&D"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.window_width = 800
        page.window_height = 700
        page.theme_mode = ft.ThemeMode.DARK

    def main(self, page: ft.Page):
        self._config_page(page)
        page.on_route_change = self.route_change
        page.go(page.route)


def start_flet_app(viwer):
    if viwer == "app":
        ft.app(target=CharacterSheetApp().main)
    elif viwer == "web":
        ft.app(target=CharacterSheetApp().main, view=ft.WEB_BROWSER)


if __name__ == "__main__":
    start_flet_app("app")
