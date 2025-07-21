import flet as ft

def habilidades_raciais_display_component(char, habilidades_raciais_repository):
    habilidades_raciais_detalhadas = char.get_habilidades_raciais_com_descricao(habilidades_raciais_repository)
    habilidades_raciais_display = []
    if habilidades_raciais_detalhadas:
        for hab in habilidades_raciais_detalhadas:
            habilidades_raciais_display.append(ft.Text(f"- {hab['nome']}: {hab['descricao']}"))
    else:
        habilidades_raciais_display.append(ft.Text("Nenhuma habilidade racial para esta raça."))
    return habilidades_raciais_display