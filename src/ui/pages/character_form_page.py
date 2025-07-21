import flet as ft


def create_character_form_page(self, page: ft.Page):
    """Cria o formulário para criar um novo personagem."""
    nome_input = ft.TextField(label="Nome do Personagem")
    jogador_input = ft.TextField(label="Nome do Jogador")

    # Dropdowns para Raça e Classe (populados dinamicamente)
    racas_disponiveis = self.raca_repository.get_all_raca_names()
    raca_dropdown = ft.Dropdown(
        label="Raça", options=[ft.dropdown.Option(r) for r in racas_disponiveis]
    )

    classes_disponiveis = self.classe_repository.get_all_classe_names()
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

    def create_character(e):
        try:
            # Validação básica
            if (
                not nome_input.value
                or not jogador_input.value
                or not raca_dropdown.value
                or not classe_dropdown.value
            ):
                page.snack_bar = ft.SnackBar(
                    ft.Text("Por favor, preencha todos os campos obrigatórios!"),
                    open=True,
                )
                page.update()
                return

            new_char = self.gerenciar_personagem_uc.criar_personagem(
                nome=nome_input.value,
                jogador=jogador_input.value,
                raca_nome=raca_dropdown.value,
                classe_nome=classe_dropdown.value,
                nivel=1,
                forca=int(forca_input.value),
                destreza=int(destreza_input.value),
                constituicao=int(constituicao_input.value),
                inteligencia=int(inteligencia_input.value),
                sabedoria=int(sabedoria_input.value),
                carisma=int(carisma_input.value),
            )
            self.current_character = (
                new_char  # Define o personagem recém-criado como o atual
            )
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Personagem '{new_char.nome}' criado com sucesso!"), open=True
            )
            page.go("/view_character")  # Vai para a tela de visualização do personagem
        except ValueError as ex:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Erro ao criar personagem: {ex}"), open=True
            )
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Um erro inesperado ocorreu: {ex}"), open=True
            )
        page.update()

    return ft.Column(
        [
            ft.Text("Criar Novo Personagem", size=20, weight=ft.FontWeight.BOLD),
            nome_input,
            jogador_input,
            raca_dropdown,
            classe_dropdown,
            ft.Text("Atributos:"),
            ft.Row([forca_input, destreza_input]),
            ft.Row([constituicao_input, inteligencia_input]),
            ft.Row([sabedoria_input, carisma_input]),
            ft.ElevatedButton("Criar Personagem", on_click=create_character),
            ft.ElevatedButton("Voltar ao Menu", on_click=lambda _: page.go("/")),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
