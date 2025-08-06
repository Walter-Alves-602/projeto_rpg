import flet as ft


def habilidades_raciais_display_component(todas_as_habilidades: list[dict[str, str]]):
    habilidades_raciais_display = []
    if todas_as_habilidades:
        for hab in todas_as_habilidades:
            habilidades_raciais_display.append(ft.Text(f"- {hab['nome']}: {hab['descricao']}"))
    else:
        habilidades_raciais_display.append(ft.Text("Nenhuma habilidade racial ou extra."))
    return habilidades_raciais_display