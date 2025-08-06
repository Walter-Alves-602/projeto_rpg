import flet as ft

from src.domain.models.usuario import PapelUsuario


def personagem_mesa_list_item(personagem, usuario_logado, on_view_click, on_delete_click):
    """Cria um item de lista para um personagem dentro da página da mesa."""

    # Define se o item é clicável (Mestre pode ver todos, Jogador só o seu)
    is_clickable = (
        usuario_logado.papel == PapelUsuario.MESTRE or
        personagem.jogador == usuario_logado.id
    )

    # Define se o botão de deletar é visível (apenas para mestres)
    show_delete_button = usuario_logado.papel == PapelUsuario.MESTRE

    item_content = ft.Row(
        [
            ft.Column(
                [
                    ft.Text(f"{personagem.nome}", weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(f"Jogador: {personagem.jogador}"), # Idealmente, buscar o nome do jogador
                    ft.Text(f"HP: {personagem.pontos_de_vida_atual}/{personagem.pontos_de_vida_max} | Nível: {personagem.nivel}"),
                ],
                expand=True,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    if show_delete_button:
        item_content.controls.append(
            ft.IconButton(
                icon=ft.Icons.DELETE_FOREVER,
                icon_color=ft.Colors.RED_400,
                tooltip="Excluir Personagem da Mesa",
                on_click=lambda e: on_delete_click(personagem.id),
            )
        )

    return ft.Container(
        padding=15,
        border=ft.border.all(1, ft.Colors.GREY_800),
        border_radius=8,
        on_click=lambda e: on_view_click(personagem) if is_clickable else None,
        bgcolor=ft.Colors.GREY_900 if is_clickable else ft.Colors.BLACK12,
        ink=is_clickable, # Efeito de clique
    )
