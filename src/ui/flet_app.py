import flet as ft
import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Importa os use cases e repositórios necessários
from src.persistence.database_manager import DatabaseManager
from src.infrastructure.adapters.database.sqlite_character_repository import (
    SQLitePersonagemRepository,
)
from src.infrastructure.adapters.data_files.racas_adapter import RacaFileAdapter
from src.infrastructure.adapters.data_files.classes_adapter import ClasseFileAdapter
from src.infrastructure.adapters.data_files.habilidades_raciais_file_adapter import (
    HabilidadesRaciaisFileAdapter,
)
from src.infrastructure.adapters.data_files.spells_file_adapter import SpellFileAdapter
from src.application.use_cases.gerenciar_personagem_use_case import (
    GerenciarPersonagemUseCase,
)
from src.ui.pages.character_sheet_page import character_sheet_page
from src.ui.pages.character_list_page import character_list_page
from src.ui.pages.character_form_page import create_character_form_page
from src.ui.pages.main_menu_page import main_menu


class CharacterSheetApp:
    def __init__(self):
        # Inicializa as dependências do seu aplicativo
        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()

        self.raca_repository = RacaFileAdapter()
        self.classe_repository = ClasseFileAdapter()
        self.habilidades_raciais_repository = HabilidadesRaciaisFileAdapter()
        self.spell_repository = SpellFileAdapter()

        self.personagem_repository = SQLitePersonagemRepository(
            self.db_manager,
            self.raca_repository,
            self.classe_repository,
            self.habilidades_raciais_repository,
        )

        self.gerenciar_personagem_uc = GerenciarPersonagemUseCase(
            self.personagem_repository,
            self.raca_repository,
            self.classe_repository,
            self.habilidades_raciais_repository,
            self.spell_repository,
        )

        self.current_character = None  # Para armazenar o personagem atualmente exibido
        self.atributo_rodado = None  # Guarda o último atributo clicado
        self.resultado_teste_atributo = {}  # Novo: guarda o resultado do teste de cada atributo

    def _create_character_form(self, page: ft.Page):
        return create_character_form_page(self, page)

    def _view_character_list(self, page: ft.Page):
        return character_list_page(self, page)

    def _display_character_sheet(self, page: ft.Page):
        return character_sheet_page(self, page)

    def _main_menu(self, page: ft.Page):
        return main_menu(self, page)

    def route_change(self, route):
        page = route.page
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [self._main_menu(page)],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        if page.route == "/create_character":
            page.views.append(
                ft.View(
                    "/create_character",
                    [self._create_character_form(page)],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE,
                )
            )
        elif page.route == "/list_characters":
            page.views.append(
                ft.View(
                    "/list_characters",
                    [self._view_character_list(page)],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE,
                )
            )
        elif page.route == "/view_character":
            page.views.append(
                ft.View(
                    "/view_character",
                    [self._display_character_sheet(page)],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE,
                )
            )

        page.update()

    def main(self, page: ft.Page):
        page.title = "Gerenciador de Personagens D&D"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.window_width = 800
        page.window_height = 700
        page.theme_mode = ft.ThemeMode.DARK  # Ou LIGHT para tema claro

        # Configura as rotas para navegação entre as telas
        page.on_route_change = self.route_change
        page.go(page.route)  # Inicia na rota atual (que será "/")


def start_flet_app():
    # Inicia o aplicativo Flet
    ft.app(target=CharacterSheetApp().main)  # Para modo normal
    # ft.app(target=CharacterSheetApp().main, view=ft.WEB_BROWSER) # Para modo web (abre no navegador)


if __name__ == "__main__":
    start_flet_app()
