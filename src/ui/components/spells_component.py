import flet as ft


def spells_display_component(magias_da_classe, classe_nome):
    magias_display = []
    if magias_da_classe:
        for magia in magias_da_classe:
            magias_display.append(
                ft.Text(f"- {magia['nome']} (Nível {magia['nivel']}, Escola: {magia['escola']})")
            )
    else:
        magias_display.append(ft.Text(f"Nenhuma magia para a classe {classe_nome}."))
    return magias_display