import flet as ft

from src.domain.models.usuario import PapelUsuario
from src.ui.components.personagem_mesa_list_item import \
    personagem_mesa_list_item
from src.ui.components.usuario_mesa_list_item import usuario_mesa_list_item


def mesa_view_page(app, page: ft.Page):
    """Cria a página de visualização e gerenciamento de uma mesa de RPG."""

    if not app.current_mesa:
        return ft.Column([ft.Text("Nenhuma mesa selecionada. Volte e selecione uma.")])

    mesa = app.current_mesa
    usuario_logado = app.current_user

    # --- Diálogos de Confirmação e Edição ---
    def show_dialog(dialog):
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Diálogo para editar a mesa
    nome_edit_field = ft.TextField(label="Nome da Mesa", value=mesa.nome)
    desc_edit_field = ft.TextField(label="Descrição", value=mesa.descricao, multiline=True)
    edit_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar Mesa"),
        content=ft.Column([nome_edit_field, desc_edit_field]),
        actions=[
            ft.TextButton("Salvar", on_click=lambda e: close_dialog("save")),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog("cancel")),
        ],
    )

    # Diálogo para adicionar usuário
    username_add_field = ft.TextField(label="Nome do Usuário")
    add_user_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Adicionar Usuário à Mesa"),
        content=ft.Column([username_add_field]),
        actions=[
            ft.TextButton("Adicionar", on_click=lambda e: close_dialog("add_user")),
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog("cancel")),
        ],
    )

    # Diálogo de confirmação genérico
    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Ação"),
        content=ft.Text("Você tem certeza?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: close_dialog("confirm")),
            ft.TextButton("Não", on_click=lambda e: close_dialog("cancel")),
        ],
    )

    def close_dialog(action):
        page.dialog.open = False
        page.update()
        # Aqui viria a lógica para cada ação
        print(f"Diálogo fechado com a ação: {action}")

    # --- Lógica de Ações ---
    def handle_view_personagem(personagem):
        app.current_character = personagem
        page.go("/view_character")

    def handle_delete_personagem(personagem_id):
        show_dialog(confirm_dialog) # Lógica de deleção viria no close_dialog

    def handle_remove_user(usuario_id):
        show_dialog(confirm_dialog) # Lógica de remoção viria no close_dialog

    # --- Construção das Listas ---
    # Lista de Personagens
    personagens_list = ft.Column(spacing=10)
    personagens_na_mesa = app.personagem_repository.listar_por_ids(mesa.personagens)
    if not personagens_na_mesa:
        personagens_list.controls.append(ft.Text("Nenhum personagem nesta mesa ainda."))
    else:
        for p in personagens_na_mesa:
            personagens_list.controls.append(
                personagem_mesa_list_item(p, usuario_logado, handle_view_personagem, handle_delete_personagem)
            )

    # Lista de Usuários
    usuarios_list = ft.Column(spacing=5)
    user_ids = mesa.mestres + mesa.jogadores
    # Implementar busca de usuários por IDs no repositório seria o ideal
    # Por agora, vamos buscar um por um (não eficiente, mas funciona)
    for user_id in user_ids:
        user = app.usuario_repository.buscar_por_id(user_id)
        if user:
            usuarios_list.controls.append(
                usuario_mesa_list_item(user, usuario_logado, handle_remove_user)
            )

    # --- Layout Final da Página ---
    return ft.Column(
        [
            # Topo: Informações da Mesa
            ft.Row([
                ft.Text(mesa.nome, size=24, weight=ft.FontWeight.BOLD, expand=True),
                ft.IconButton(ft.Icons.EDIT, on_click=lambda e: show_dialog(edit_dialog), tooltip="Editar Mesa"),
            ]),
            ft.Text(mesa.descricao or "Sem descrição.", italic=True),
            ft.Divider(),

            # Meio: Lista de Personagens
            ft.Text("Personagens na Mesa", size=20, weight=ft.FontWeight.BOLD),
            personagens_list,
            ft.Divider(),

            # Fundo: Lista de Usuários
            ft.Row([
                ft.Text("Participantes", size=20, weight=ft.FontWeight.BOLD, expand=True),
                ft.ElevatedButton("Adicionar Usuário", icon=ft.Icons.ADD, on_click=lambda e: show_dialog(add_user_dialog), visible=(usuario_logado.papel == PapelUsuario.MESTRE)),
            ]),
            usuarios_list,
            ft.Divider(),

            ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/list_characters")),
        ],
        spacing=15,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )
