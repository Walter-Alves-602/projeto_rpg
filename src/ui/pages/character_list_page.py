import flet as ft

def character_list_page(self, page: ft.Page):
    """Cria a lista de personagens existentes."""
    characters = self.gerenciar_personagem_uc.listar_todos_personagens()
    
    def select_character(e):
        character_name = e.control.data # O nome do personagem está no dado do botão
        self.current_character = self.gerenciar_personagem_uc.obter_personagem_por_nome(character_name)
        if self.current_character:
            page.go("/view_character")
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: Personagem '{character_name}' não encontrado."), open=True)
            page.update()

    list_controls = []
    if not characters:
        list_controls.append(ft.Text("Nenhum personagem cadastrado. Crie um novo!"))
    else:
        for char in characters:
            list_controls.append(
                ft.ElevatedButton(
                    f"{char.nome} (Raça: {char.raca_nome}, Classe: {char.classe_nome})",
                    on_click=select_character,
                    data=char.nome # Armazena o nome do personagem no botão
                )
            )

    return ft.Column(
        [
            ft.Text("Personagens Existentes", size=20, weight=ft.FontWeight.BOLD),
            *list_controls, # Desempacota a lista de botões
            ft.ElevatedButton("Voltar ao Menu", on_click=lambda _: page.go("/")),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )