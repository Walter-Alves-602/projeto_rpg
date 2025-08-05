import flet as ft

from src.domain.models.usuario import PapelUsuario

cargos = ("Player", "Master")

def _get_options():
    options = []
    for cargo in cargos:
        options.append(
            ft.DropdownOption(
                key=cargo,
                content=ft.Text(cargo),
            )
        )
    return options

def register_page(app, page: ft.Page):
    """Cria a página de registro."""
    nome_field = ft.TextField(label="Nome de Usuário", width=300)
    senha_field = ft.TextField(label="Senha", password=True, width=300)
    confirmar_senha_field = ft.TextField(label="Confirmar Senha", password=True, width=300)
    funcao_dropdown = ft.Dropdown(label="Função", options=_get_options(), width=300)
    error_message = ft.Text("", color=ft.Colors.RED_500)

    def register_button_click(e):
        if senha_field.value != confirmar_senha_field.value:
            error_message.value = "As senhas não coincidem!"
            page.update()
            return

        if not funcao_dropdown.value:
            error_message.value = "Por favor, selecione uma função (Player/Master)."
            page.update()
            return

        papel = PapelUsuario.JOGADOR if funcao_dropdown.value == "Player" else PapelUsuario.MESTRE

        try:
            app.registrar_usuario(nome_field.value, senha_field.value, papel)
            page.go("/login") # Redireciona para o login após o registro
        except ValueError as e:
            error_message.value = str(e)
            page.update()

    btn_cadastrar = ft.ElevatedButton("Cadastrar", on_click=register_button_click)
    btn_voltar = ft.TextButton("Voltar ao Login", on_click=lambda _: page.go("/login"))    

    return ft.Column(
        [
            ft.Text("Registro", size=24, weight=ft.FontWeight.BOLD),
            nome_field,
            senha_field,
            confirmar_senha_field,
            funcao_dropdown,
            btn_cadastrar,
            btn_voltar,
            error_message
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )

