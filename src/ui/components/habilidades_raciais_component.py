import flet as ft

def habilidades_raciais_display_component(char, habilidades_raciais_repository):
    habilidades_raciais_detalhadas = char.get_habilidades_raciais_com_descricao(habilidades_raciais_repository)
    habilidades_extras = char.habilidades_extras

    # Combina as habilidades raciais e as extras em uma única lista
    todas_as_habilidades = habilidades_raciais_detalhadas + habilidades_extras

    habilidades_raciais_display = []
    if todas_as_habilidades:
        for hab in todas_as_habilidades:
            habilidades_raciais_display.append(ft.Text(f"- {hab['nome']}: {hab['descricao']}"))
    else:
        habilidades_raciais_display.append(ft.Text("Nenhuma habilidade racial ou extra."))
    return habilidades_raciais_display