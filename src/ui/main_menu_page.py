import flet as ft

def main_menu(self, page: ft.Page):
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