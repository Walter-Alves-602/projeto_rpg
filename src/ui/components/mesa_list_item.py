import flet as ft


def mesa_list_item(mesa, mestre_nome, personagem_nome, on_details_click):
    """Cria um item de lista para uma mesa."""
    return ft.Container(
        padding=10,
        border=ft.border.all(1, ft.Colors.GREY_700),
        border_radius=8,
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(f"Mesa: {mesa.nome}", weight=ft.FontWeight.BOLD),
                        ft.Text(f"Mestre: {mestre_nome}"),
                        ft.Text(f"Personagem: {personagem_nome or 'N/A'}"),
                    ],
                    expand=True,
                ),
                ft.ElevatedButton(
                    "Entrar",
                    on_click=lambda e: on_details_click(mesa.id),
                    icon=ft.Icons.LOGIN,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
