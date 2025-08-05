import flet as ft

def login_page(app, page: ft.Page):
    """Cria a página de login."""

    username_field = ft.TextField(label="Nome de Usuário", width=300, autofocus=True)
    password_field = ft.TextField(label="Senha", password=True, width=300)
    error_message = ft.Text("", color=ft.Colors.RED_500)

    def login_button_click(e):
        user = app.autenticar_usuario(username_field.value, password_field.value)
        if user:
            page.go("/dashboard")  # Assuming successful login goes to dashboard
        else:
            error_message.value = "Nome de usuário ou senha inválidos."
            page.update()

    def register_button_click(e):
        page.go("/register")

    login_button = ft.ElevatedButton(text="Login", on_click=login_button_click)
    register_button = ft.TextButton(
        text="Não tem uma conta? Registre-se", on_click=register_button_click
    )

    return ft.Column(
        [
            ft.Text("Login", size=24, weight=ft.FontWeight.BOLD),
            username_field,
            password_field,
            login_button,
            register_button,
            error_message
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )
