import flet as ft

def habilidades_extras_component(habilidades_extras: list[dict[str, str]], on_remove):
    """
    Exibe habilidades extras com nome, descrição e botão de remover.
    :param habilidades_extras: lista de dicts com 'nome' e 'descricao'
    :param on_remove: função callback que recebe o nome da habilidade a ser removida
    """
    if not habilidades_extras:
        return [ft.Text("Nenhuma habilidade extra.")]

    display = []
    for hab in habilidades_extras:
        row = ft.Row([
            ft.Text(f"{hab['nome']}: {hab['descricao']}", expand=True),
            ft.IconButton(
                icon=ft.icons.DELETE,
                tooltip="Remover",
                on_click=lambda e, nome=hab['nome']: on_remove(nome)
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        display.append(row)
    return display
