import flet as ft

from src.domain.models import PapelUsuario


def usuario_mesa_list_item(usuario, usuario_logado, on_remove_click):
    """Cria um item de lista para um usuário dentro da página da mesa."""

    # O botão de remover só aparece para mestres e não pode remover a si mesmo
    show_remove_button = (
        usuario_logado.papel == PapelUsuario.MESTRE and
        usuario.id != usuario_logado.id
    )

    return ft.ListTile(
        leading=ft.Icon(ft.Icons.PERSON),
        title=ft.Text(f"{usuario.username} ({usuario.papel.value})"),
        trailing=ft.IconButton(
            icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
            icon_color=ft.Colors.RED_400,
            tooltip="Remover Usuário da Mesa",
            on_click=lambda e: on_remove_click(usuario.id),
            visible=show_remove_button,
        ),
    )
