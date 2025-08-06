import flet as ft
from src.domain.models.usuario import PapelUsuario
from src.ui.components.mesa_list_item import mesa_list_item

def character_list_page(app, page: ft.Page):
    """Cria a página que lista as mesas do usuário e permite a criação de novas mesas para mestres."""

    # --- Formulário de Criação de Mesa (para Mestres) ---
    nome_mesa_field = ft.TextField(label="Nome da Mesa", width=300)
    descricao_mesa_field = ft.TextField(label="Descrição", multiline=True, width=300)
    error_text = ft.Text("", color=ft.Colors.RED_500, visible=False)

    def criar_mesa_click(e):
        error_text.visible = False # Esconde a mensagem de erro anterior
        if not nome_mesa_field.value:
            error_text.value = "O nome da mesa é obrigatório."
            error_text.visible = True
            page.update()
            return

        try:
            app.gerenciar_mesa_uc.criar_mesa(
                nome=nome_mesa_field.value,
                descricao=descricao_mesa_field.value,
                mestre_id=app.current_user.id,
            )
            # Limpa os campos e recarrega a página para mostrar a nova mesa
            nome_mesa_field.value = ""
            descricao_mesa_field.value = ""
            page.go("/list_characters") # Recarrega a view
        except Exception as ex:
            error_text.value = f"Erro ao criar mesa: {ex}"
            error_text.visible = True
            page.update()

    form_criacao_mesa = ft.ExpansionPanelList(
        expand_icon_color=ft.Colors.AMBER,
        elevation=4,
        divider_color=ft.Colors.AMBER,
        controls=[
            ft.ExpansionPanel(
                header=ft.ListTile(title=ft.Text("Criar Nova Mesa de RPG", weight=ft.FontWeight.BOLD)),
                content=ft.Container(
                    padding=15,
                    content=ft.Column(
                        [
                            nome_mesa_field,
                            descricao_mesa_field,
                            error_text, # Adiciona o campo de texto de erro aqui
                            ft.ElevatedButton("Criar Mesa", on_click=criar_mesa_click, icon=ft.Icons.ADD),
                        ],
                        spacing=15,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
            )
        ]
    )

    # --- Lógica de Exibição da Lista de Mesas ---
    def on_details_click(mesa_id):
        mesa = app.gerenciar_mesa_uc.buscar_mesa_por_id(mesa_id)
        if mesa:
            app.current_mesa = mesa
            page.go("/view_mesa")

    list_controls = []
    if not app.current_user:
        list_controls.append(ft.Text("Faça o login para ver suas mesas."))
    else:
        mesas_do_usuario = app.gerenciar_mesa_uc.listar_mesas_do_usuario(app.current_user.id)

        if not mesas_do_usuario:
            list_controls.append(ft.Container(ft.Text("Você ainda não participa de nenhuma mesa."), padding=20))
        else:
            for mesa in mesas_do_usuario:
                mestre_principal_id = mesa.mestres[0] if mesa.mestres else None
                mestre_user = app.usuario_repository.buscar_por_id(mestre_principal_id) if mestre_principal_id else None
                mestre_nome = mestre_user.username if mestre_user else "Desconhecido"

                personagem_nome = None
                if mesa.personagens:
                    personagens_na_mesa = app.personagem_repository.listar_por_ids(mesa.personagens)
                    personagem_do_usuario = next((p for p in personagens_na_mesa if p.jogador == app.current_user.id), None)
                    if personagem_do_usuario:
                        personagem_nome = personagem_do_usuario.nome

                list_controls.append(
                    mesa_list_item(
                        mesa=mesa,
                        mestre_nome=mestre_nome,
                        personagem_nome=personagem_nome,
                        on_details_click=on_details_click,
                    )
                )

    # --- Layout Final da Página ---
    page_content = [
        ft.Text("Minhas Mesas de RPG", size=24, weight=ft.FontWeight.BOLD),
    ]

    # Adiciona o formulário de criação apenas se o usuário for um mestre
    if app.current_user and app.current_user.papel == PapelUsuario.MESTRE:
        page_content.append(form_criacao_mesa)

    page_content.extend([
        ft.Divider(height=20, color=ft.Colors.GREY_800),
        ft.Column(list_controls, spacing=15, expand=True, scroll=ft.ScrollMode.AUTO),
        ft.ElevatedButton("Voltar ao Menu", on_click=lambda _: page.go("/main_menu")),
    ])

    return ft.Column(
        page_content,
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )
