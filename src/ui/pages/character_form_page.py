import flet as ft

def create_character_form_page(app, page: ft.Page):
    """Cria o formulário para criar um novo personagem."""
    nome_input = ft.TextField(label="Nome do Personagem")
    # Removido jogador_input, pois o jogador será o current_user

    # Dropdowns para Raça e Classe (populados dinamicamente)
    racas_disponiveis = app.raca_repository.get_all_raca_names()
    raca_dropdown = ft.Dropdown(
        label="Raça", options=[ft.dropdown.Option(r) for r in racas_disponiveis]
    )

    classes_disponiveis = app.classe_repository.get_all_classe_names()
    classe_dropdown = ft.Dropdown(
        label="Classe", options=[ft.dropdown.Option(c) for c in classes_disponiveis]
    )

    # Campos de atributos
    forca_input = ft.TextField(
        label="Força", value="10", keyboard_type=ft.KeyboardType.NUMBER
    )
    destreza_input = ft.TextField(
        label="Destreza", value="10", keyboard_type=ft.KeyboardType.NUMBER
    )
    constituicao_input = ft.TextField(
        label="Constituição", value="10", keyboard_type=ft.KeyboardType.NUMBER
    )
    inteligencia_input = ft.TextField(
        label="Inteligência", value="10", keyboard_type=ft.KeyboardType.NUMBER
    )
    sabedoria_input = ft.TextField(
        label="Sabedoria", value="10", keyboard_type=ft.KeyboardType.NUMBER
    )
    carisma_input = ft.TextField(
        label="Carisma", value="10", keyboard_type=ft.KeyboardType.NUMBER
    )

    error_message = ft.Text("", color=ft.Colors.RED_500, visible=False)

    def create_character(e):
        error_message.visible = False # Esconde a mensagem de erro anterior
        try:
            # Validação básica
            if (
                not nome_input.value
                or not raca_dropdown.value
                or not classe_dropdown.value
            ):
                error_message.value = "Preencha todos os campos obrigatórios!"
                error_message.visible = True
                page.update()
                return

            dados_personagem = {
                "nome": nome_input.value,
                "jogador": app.current_user.id, # Usar o ID do usuário logado
                "raca_nome": raca_dropdown.value,
                "classe_nome": classe_dropdown.value,
                "nivel": 1,
                "pontos_de_experiencia": 0,
                "forca": int(forca_input.value),
                "destreza": int(destreza_input.value),
                "constituicao": int(constituicao_input.value),
                "inteligencia": int(inteligencia_input.value),
                "sabedoria": int(sabedoria_input.value),
                "carisma": int(carisma_input.value),
            }

            new_char = app.gerenciar_personagem_uc.criar_personagem(dados_personagem)
            app.current_character = new_char  # Define o personagem recém-criado como o atual

            page.go("/user_page")  # Vai para a tela de visualização do personagem
        except ValueError as ex:
            error_message.value = f"Erro ao criar personagem: {ex}"
            error_message.visible = True
            page.update()
        except Exception as ex:
            error_message.value = f"Erro inesperado: {ex}"
            error_message.visible = True
            page.update()

        page.update()

    return ft.Column(
        [
            ft.Text("Criar Novo Personagem", size=20, weight=ft.FontWeight.BOLD),
            nome_input,
            raca_dropdown,
            classe_dropdown,
            ft.Text("Atributos:"),
            ft.Row([forca_input, destreza_input]),
            ft.Row([constituicao_input, inteligencia_input]),
            ft.Row([sabedoria_input, carisma_input]),
            error_message, # Adiciona o campo de texto de erro aqui
            ft.ElevatedButton("Criar Personagem", on_click=create_character),
            ft.ElevatedButton("Voltar ao Menu", on_click=lambda _: page.go("/user_page")),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
