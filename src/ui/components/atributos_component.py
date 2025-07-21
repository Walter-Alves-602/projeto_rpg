import flet as ft

def atributos_display_component(char, atributo_rodado, on_atributo_click, resultados):
    atributos_display = []
    for attr, val in char.atributos.items():
        mod = char.modificadores_atributo[attr]
        row = [
            ft.ElevatedButton(
                f"{attr.capitalize()}: {val} (Mod: {'+' if mod >= 0 else ''}{mod})",
                on_click=on_atributo_click,
                data=attr
            )
        ]
        if atributo_rodado == attr:
            resultado = resultados.get(attr)
            if resultado is not None:
                row.append(ft.Text(f"Resultado: {resultado}", color=ft.Colors.GREEN))
        atributos_display.append(ft.Row(row, spacing=10))
    return atributos_display