import flet as ft
from src.ui.components import atributos_display_component, habilidades_raciais_display_component, spells_display_component, habilidade_imput
from src.domain.services import DiceRoller



def character_sheet_page(app, page):
    char = app.current_character

    if not char:
        page.go("/")
        page.update()
        return ft.Column([ft.Text("...")])

    def on_atributo_click(e):
        atributo = e.control.data
        mod = char.modificadores_atributo[atributo]
        resultado = DiceRoller.roll(20, 1, mod)
        app.resultado_teste_atributo[atributo] = resultado
        app.atributo_rodado = atributo
        page.views[-1].controls = [character_sheet_page(app, page)]
        page.update()

    atributos_display = atributos_display_component(
        char,
        app.atributo_rodado,
        on_atributo_click,
        app.resultado_teste_atributo  # novo parâmetro
    )

    def handle_add_habilidade(nome_habilidade: str, descricao_habilidade: str):
        """
        Callback para o componente de input. Chama o UseCase e atualiza a UI.
        """
        if not nome_habilidade or not descricao_habilidade:
            # Poderíamos adicionar um snackbar de erro aqui no futuro
            return

        # Chama o UseCase para adicionar a habilidade e persistir
        updated_char = app.gerenciar_personagem_uc.adicionar_habilidade_extra(
            char.nome, nome_habilidade, descricao_habilidade
        )
        app.current_character = updated_char  # Atualiza o personagem atual no app
        # Força a recriação e atualização da view com os novos dados
        page.views[-1].controls = [character_sheet_page(app, page)]
        page.update()

    # Busca as habilidades através do UseCase
    todas_as_habilidades = app.gerenciar_personagem_uc.obter_habilidades_com_descricao(char.nome)
    habilidades_raciais_display = habilidades_raciais_display_component(todas_as_habilidades)
    magias_da_classe = app.spell_repository.get_spells_by_class(char.classe_nome)
    magias_display = spells_display_component(magias_da_classe, char.classe_nome)

    hp_input = ft.TextField(
        label="Pontos de Vida (Atual)",
        value=str(char.pontos_de_vida_atual),
        keyboard_type=ft.KeyboardType.NUMBER,
        read_only=True
    )

    def take_damage_or_heal(e):
        try:
            amount = int(e.control.data)
            if e.control.text == "Tomar Dano":
                char.pontos_de_vida_atual = max(0, char.pontos_de_vida_atual - amount)
            elif e.control.text == "Curar":
                char.pontos_de_vida_atual = min(char.pontos_de_vida_max, char.pontos_de_vida_atual + amount)
            app.gerenciar_personagem_uc._personagem_repository.save(char)
            hp_input.value = str(char.pontos_de_vida_atual)
            page.update()
        except ValueError:
            page.update()

    return ft.Column(
        [
            ft.Text(f"Ficha de Personagem: {char.nome}", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            # nome e informaçoes 
            ft.Row([
                ft.Column([
                    ft.Text(f"Jogador: {char.jogador}"),
                    ft.Text(f"Raça: {char.raca_nome}"),
                    ft.Text(f"Classe: {char.classe_nome}"),
                    ft.Text(f"Nível: {char.nivel}"),
                    ft.Row([
                        ft.Text(f"PV: {char.pontos_de_vida_atual}/{char.pontos_de_vida_max}"),
                        ft.ElevatedButton("Tomar Dano", on_click=take_damage_or_heal, data="5"),
                        ft.ElevatedButton("Curar", on_click=take_damage_or_heal, data="5")
                    ])
                ]),
                ft.Column([
                    *atributos_display
                ])
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            # Habilidades raciais
            ft.Text("Habilidades Raciais", size=18, weight=ft.FontWeight.BOLD),
            habilidade_imput(on_add=handle_add_habilidade),
            *habilidades_raciais_display,
            ft.Divider(),
            ft.Text("Magias da Classe", size=18, weight=ft.FontWeight.BOLD),
            *magias_display,
            ft.ElevatedButton("Voltar à Lista", on_click=lambda _: page.go("/list_characters")),
            ft.ElevatedButton("Voltar ao Menu Principal", on_click=lambda _: page.go("/")),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.ADAPTIVE
    )