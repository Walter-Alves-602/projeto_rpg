# src/ui/flet_app.py
import flet as ft
import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Importa os use cases e repositórios necessários
from src.persistence.database_manager import DatabaseManager
from src.infrastructure.adapters.database.sqlite_character_repository import SQLitePersonagemRepository
from src.infrastructure.adapters.data_files.racas_adapter import RacaFileAdapter
from src.infrastructure.adapters.data_files.classes_adapter import ClasseFileAdapter
from src.infrastructure.adapters.data_files.habilidades_raciais_file_adapter import HabilidadesRaciaisFileAdapter
from src.infrastructure.adapters.data_files.spells_file_adapter import SpellFileAdapter
from src.application.use_cases.gerenciar_personagem_use_case import GerenciarPersonagemUseCase

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
            self.habilidades_raciais_repository
        )

        self.gerenciar_personagem_uc = GerenciarPersonagemUseCase(
            self.personagem_repository,
            self.raca_repository,
            self.classe_repository,
            self.habilidades_raciais_repository,
            self.spell_repository
        )

        self.current_character = None # Para armazenar o personagem atualmente exibido

    def _create_character_form(self, page: ft.Page):
        """Cria o formulário para criar um novo personagem."""
        nome_input = ft.TextField(label="Nome do Personagem")
        jogador_input = ft.TextField(label="Nome do Jogador")

        # Dropdowns para Raça e Classe (populados dinamicamente)
        racas_disponiveis = self.raca_repository.get_all_raca_names()
        raca_dropdown = ft.Dropdown(
            label="Raça",
            options=[ft.dropdown.Option(r) for r in racas_disponiveis]
        )

        classes_disponiveis = self.classe_repository.get_all_classe_names()
        classe_dropdown = ft.Dropdown(
            label="Classe",
            options=[ft.dropdown.Option(c) for c in classes_disponiveis]
        )

        # Campos de atributos
        forca_input = ft.TextField(label="Força", value="10", keyboard_type=ft.KeyboardType.NUMBER)
        destreza_input = ft.TextField(label="Destreza", value="10", keyboard_type=ft.KeyboardType.NUMBER)
        constituicao_input = ft.TextField(label="Constituição", value="10", keyboard_type=ft.KeyboardType.NUMBER)
        inteligencia_input = ft.TextField(label="Inteligência", value="10", keyboard_type=ft.KeyboardType.NUMBER)
        sabedoria_input = ft.TextField(label="Sabedoria", value="10", keyboard_type=ft.KeyboardType.NUMBER)
        carisma_input = ft.TextField(label="Carisma", value="10", keyboard_type=ft.KeyboardType.NUMBER)

        def create_character(e):
            try:
                # Validação básica
                if not nome_input.value or not jogador_input.value or not raca_dropdown.value or not classe_dropdown.value:
                    page.snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos obrigatórios!"), open=True)
                    page.update()
                    return

                new_char = self.gerenciar_personagem_uc.criar_personagem(
                    nome=nome_input.value,
                    jogador=jogador_input.value,
                    raca_nome=raca_dropdown.value,
                    classe_nome=classe_dropdown.value,
                    nivel=1,
                    forca=int(forca_input.value),
                    destreza=int(destreza_input.value),
                    constituicao=int(constituicao_input.value),
                    inteligencia=int(inteligencia_input.value),
                    sabedoria=int(sabedoria_input.value),
                    carisma=int(carisma_input.value)
                )
                self.current_character = new_char # Define o personagem recém-criado como o atual
                page.snack_bar = ft.SnackBar(ft.Text(f"Personagem '{new_char.nome}' criado com sucesso!"), open=True)
                page.go("/view_character") # Vai para a tela de visualização do personagem
            except ValueError as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao criar personagem: {ex}"), open=True)
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Um erro inesperado ocorreu: {ex}"), open=True)
            page.update()


        return ft.Column(
            [
                ft.Text("Criar Novo Personagem", size=20, weight=ft.FontWeight.BOLD),
                nome_input,
                jogador_input,
                raca_dropdown,
                classe_dropdown,
                ft.Text("Atributos:"),
                ft.Row([forca_input, destreza_input]),
                ft.Row([constituicao_input, inteligencia_input]),
                ft.Row([sabedoria_input, carisma_input]),
                ft.ElevatedButton("Criar Personagem", on_click=create_character),
                ft.ElevatedButton("Voltar ao Menu", on_click=lambda _: page.go("/")),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def _view_character_list(self, page: ft.Page):
        """Cria a lista de personagens existentes."""
        characters = self.gerenciar_personagem_uc.listar_todos_personagens()
        
        def select_character(e):
            character_name = e.control.data # O nome do personagem está no dado do botão
            self.current_character = self.gerenciar_personagem_uc.obter_personagem_por_nome(character_name)
            if self.current_character:
                page.go("/view_character")
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro: Personagem '{character_name}' não encontrado."), open=True)
                page.update()

        list_controls = []
        if not characters:
            list_controls.append(ft.Text("Nenhum personagem cadastrado. Crie um novo!"))
        else:
            for char in characters:
                list_controls.append(
                    ft.ElevatedButton(
                        f"{char.nome} (Raça: {char.raca_nome}, Classe: {char.classe_nome})",
                        on_click=select_character,
                        data=char.nome # Armazena o nome do personagem no botão
                    )
                )

        return ft.Column(
            [
                ft.Text("Personagens Existentes", size=20, weight=ft.FontWeight.BOLD),
                *list_controls, # Desempacota a lista de botões
                ft.ElevatedButton("Voltar ao Menu", on_click=lambda _: page.go("/")),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def _display_character_sheet(self, page: ft.Page):
        """Exibe a ficha detalhada do personagem atual."""
        if not self.current_character:
            # Redireciona de volta se não houver personagem selecionado
            page.go("/")
            page.snack_bar = ft.SnackBar(ft.Text("Nenhum personagem selecionado."), open=True)
            page.update()
            return ft.Column([ft.Text("...")]) # Placeholder enquanto redireciona

        char = self.current_character

        # Exibição de atributos e modificadores
        atributos_display = []
        for attr, val in char.atributos.items():
            mod = char.modificadores_atributo[attr]
            atributos_display.append(ft.Text(f"{attr.capitalize()}: {val} (Mod: {'+' if mod >= 0 else ''}{mod})"))

        # Exibição de habilidades raciais
        habilidades_raciais_detalhadas = char.get_habilidades_raciais_com_descricao(self.habilidades_raciais_repository)
        habilidades_raciais_display = []
        if habilidades_raciais_detalhadas:
            for hab in habilidades_raciais_detalhadas:
                habilidades_raciais_display.append(ft.Text(f"- {hab['nome']}: {hab['descricao']}"))
        else:
            habilidades_raciais_display.append(ft.Text("Nenhuma habilidade racial para esta raça."))

        # Exibição de Magias da Classe
        magias_da_classe = self.spell_repository.get_spells_by_class(char.classe_nome)
        magias_display = []
        if magias_da_classe:
            for magia in magias_da_classe:
                magias_display.append(ft.Text(f"- {magia['nome']} (Nível {magia['nivel']}, Escola: {magia['escola']})"))
        else:
            magias_display.append(ft.Text(f"Nenhuma magia para a classe {char.classe_nome}."))

        # Campos para HP (simplificado por enquanto)
        hp_input = ft.TextField(
            label="Pontos de Vida (Atual)",
            value=str(char.pontos_de_vida_atual),
            keyboard_type=ft.KeyboardType.NUMBER,
            read_only=True # Apenas para exibição inicial
        )

        def take_damage_or_heal(e):
            try:
                amount = int(e.control.data) # O valor do dano/cura está no 'data' do botão
                if e.control.text == "Tomar Dano":
                    char.pontos_de_vida_atual = max(0, char.pontos_de_vida_atual - amount)
                elif e.control.text == "Curar":
                    char.pontos_de_vida_atual = min(char.pontos_de_vida_max, char.pontos_de_vida_atual + amount)
                
                # Salva o personagem atualizado no banco de dados
                self.gerenciar_personagem_uc._personagem_repository.save(char)
                hp_input.value = str(char.pontos_de_vida_atual) # Atualiza o campo de texto
                page.update()
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Valor inválido."), open=True)
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}"), open=True)
                page.update()

        return ft.Column(
            [
                ft.Text(f"Ficha de Personagem: {char.nome}", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Jogador: {char.jogador}"),
                ft.Text(f"Raça: {char.raca_nome}"),
                ft.Text(f"Classe: {char.classe_nome}"),
                ft.Text(f"Nível: {char.nivel}"),
                
                ft.Row([
                    ft.Text(f"PV: {char.pontos_de_vida_atual}/{char.pontos_de_vida_max}"),
                    ft.ElevatedButton("Tomar Dano", on_click=take_damage_or_heal, data="5"), # Exemplo de dano 5
                    ft.ElevatedButton("Curar", on_click=take_damage_or_heal, data="5"), # Exemplo de cura 5
                ]),
                
                ft.Divider(),
                ft.Text("Atributos", size=18, weight=ft.FontWeight.BOLD),
                *atributos_display, # Desempacota a lista de textos de atributos

                ft.Divider(),
                ft.Text("Habilidades Raciais", size=18, weight=ft.FontWeight.BOLD),
                *habilidades_raciais_display,
                
                ft.Divider(),
                ft.Text("Magias da Classe", size=18, weight=ft.FontWeight.BOLD),
                *magias_display,

                ft.ElevatedButton("Voltar à Lista", on_click=lambda _: page.go("/list_characters")),
                ft.ElevatedButton("Voltar ao Menu Principal", on_click=lambda _: page.go("/")),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.ADAPTIVE # Adiciona scroll se o conteúdo for muito grande
        )

    def _main_menu(self, page: ft.Page):
        """Cria o menu principal."""
        return ft.Column(
            [
                ft.Text("Bem-vindo ao Gerenciador de Personagens D&D", size=24, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Criar Novo Personagem", on_click=lambda _: page.go("/create_character")),
                ft.ElevatedButton("Ver Personagens Existentes", on_click=lambda _: page.go("/list_characters")),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

    def route_change(self, route):
        page = route.page
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [self._main_menu(page)],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        if page.route == "/create_character":
            page.views.append(
                ft.View(
                    "/create_character",
                    [self._create_character_form(page)],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE
                )
            )
        elif page.route == "/list_characters":
            page.views.append(
                ft.View(
                    "/list_characters",
                    [self._view_character_list(page)],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE
                )
            )
        elif page.route == "/view_character":
            page.views.append(
                ft.View(
                    "/view_character",
                    [self._display_character_sheet(page)],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE
                )
            )
        
        page.update()

    def main(self, page: ft.Page):
        page.title = "Gerenciador de Personagens D&D"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.window_width = 800
        page.window_height = 700
        page.theme_mode = ft.ThemeMode.DARK # Ou LIGHT para tema claro

        # Configura as rotas para navegação entre as telas
        page.on_route_change = self.route_change
        page.go(page.route) # Inicia na rota atual (que será "/")

def start_flet_app():
    # Inicia o aplicativo Flet
    # ft.app(target=CharacterSheetApp().main) # Para modo normal
    # ft.app(target=CharacterSheetApp().main, view=ft.WEB_BROWSER) # Para modo web (abre no navegador)
    ft.app(target=CharacterSheetApp().main)


if __name__ == "__main__":
    start_flet_app()