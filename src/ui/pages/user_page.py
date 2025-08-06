import flet as ft
from src.domain.models.usuario import PapelUsuario
from src.ui.components.mesa_list_item import mesa_list_item

def user_page(app, page: ft.Page):
    """Página do usuário para gerenciar suas mesas e personagens."""

    if not app.current_user:
        return ft.Column([ft.Text("Faça o login para ver seus dados.")])

    # --- DIÁLOGOS ---
    confirm_delete_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text("Você tem certeza que deseja excluir este personagem?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: close_delete_dialog(True)),
            ft.TextButton("Não", on_click=lambda e: close_delete_dialog(False)),
        ],
    )

    def close_delete_dialog(confirmed):
        page.dialog.open = False
        page.update()
        if confirmed:
            try:
                app.gerenciar_personagem_uc.deletar_personagem(page.data_to_delete)
                page.go("/user_page") # Recarrega a página
            except Exception as ex:
                # Usar um Text para erro em vez de SnackBar
                print(f"Erro ao excluir: {ex}")

    def open_delete_confirmation(personagem_id):
        page.data_to_delete = personagem_id
        page.dialog = confirm_delete_dialog
        confirm_delete_dialog.open = True
        page.update()

    # --- SEÇÃO DE MESAS ---
    nome_mesa_field = ft.TextField(label="Nome da Mesa", width=300)
    descricao_mesa_field = ft.TextField(label="Descrição", multiline=True, width=300)
    error_text_mesa = ft.Text("", color=ft.Colors.RED_500, visible=False)

    def criar_mesa_click(e):
        error_text_mesa.visible = False
        if not nome_mesa_field.value:
            error_text_mesa.value = "O nome da mesa é obrigatório."
            error_text_mesa.visible = True
            page.update()
            return
        try:
            app.gerenciar_mesa_uc.criar_mesa(nome=nome_mesa_field.value, descricao=descricao_mesa_field.value, mestre_id=app.current_user.id)
            nome_mesa_field.value = ""
            descricao_mesa_field.value = ""
            page.go("/user_page")
        except Exception as ex:
            error_text_mesa.value = f"Erro ao criar mesa: {ex}"
            error_text_mesa.visible = True
            page.update()

    form_criacao_mesa = ft.ExpansionPanelList(
        expand_icon_color=ft.Colors.AMBER,
        controls=[
            ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text("Criar Nova Mesa de RPG")),
                content=ft.Container(padding=15, content=ft.Column([
                    nome_mesa_field, descricao_mesa_field, error_text_mesa,
                    ft.ElevatedButton("Criar Mesa", on_click=criar_mesa_click, icon=ft.Icons.ADD)
                ]))
            )
        ]
    )

    def on_mesa_details_click(mesa_id):
        mesa = app.gerenciar_mesa_uc.buscar_mesa_por_id(mesa_id)
        if mesa:
            app.current_mesa = mesa
            page.go("/view_mesa")

    mesas_list_controls = []
    mesas_do_usuario = app.gerenciar_mesa_uc.listar_mesas_do_usuario(app.current_user.id)
    if not mesas_do_usuario:
        mesas_list_controls.append(ft.Text("Você ainda não participa de nenhuma mesa."))
    else:
        for mesa in mesas_do_usuario:
            mestre_user = app.usuario_repository.buscar_por_id(mesa.mestres[0]) if mesa.mestres else None
            mestre_nome = mestre_user.username if mestre_user else "N/A"
            personagens_na_mesa = app.personagem_repository.listar_por_ids(mesa.personagens)
            personagem_do_usuario = next((p for p in personagens_na_mesa if p.jogador == app.current_user.id), None)
            personagem_nome = personagem_do_usuario.nome if personagem_do_usuario else None
            mesas_list_controls.append(mesa_list_item(mesa, mestre_nome, personagem_nome, on_mesa_details_click))

    # --- SEÇÃO DE PERSONAGENS ---
    def view_character_click(personagem):
        app.current_character = personagem
        page.go("/view_character")

    character_list_controls = []
    user_characters = app.gerenciar_personagem_uc.listar_personagens_por_jogador(app.current_user.id)
    if not user_characters:
        character_list_controls.append(ft.Text("Você ainda não criou nenhum personagem."))
    else:
        for char in user_characters:
            character_list_controls.append(ft.Container(padding=10, border=ft.border.all(1, ft.Colors.GREY_700), border_radius=8, content=ft.Row([
                ft.Column([ft.Text(f"{char.nome}", weight=ft.FontWeight.BOLD), ft.Text(f"Raça: {char.raca_nome}, Classe: {char.classe_nome}, Nível: {char.nivel}")], expand=True),
                ft.ElevatedButton("Ver Ficha", on_click=lambda e, c=char: view_character_click(c)),
                ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e, c_id=char.id: open_delete_confirmation(c_id), tooltip="Excluir Personagem"),
            ])))

    # --- LAYOUT FINAL ---
    page_content = [
        ft.Text(f"Painel de {app.current_user.username}", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("Minhas Mesas de RPG", size=20, weight=ft.FontWeight.BOLD),
    ]
    if app.current_user.papel == PapelUsuario.MESTRE:
        page_content.append(form_criacao_mesa)
    page_content.append(ft.Column(mesas_list_controls, spacing=15, scroll=ft.ScrollMode.AUTO))
    page_content.extend([
        ft.Divider(),
        ft.Row([ft.Text("Meus Personagens", size=20, weight=ft.FontWeight.BOLD, expand=True), ft.ElevatedButton("Criar Novo Personagem", icon=ft.Icons.ADD, on_click=lambda _: page.go("/create_character"))]),
        ft.Column(character_list_controls, spacing=10, scroll=ft.ScrollMode.AUTO),
        ft.Divider(),
        ft.ElevatedButton("Voltar ao Menu Principal", on_click=lambda _: page.go("/main_menu")),
    ])

    return ft.Column(page_content, spacing=15, expand=True, scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
