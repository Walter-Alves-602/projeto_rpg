import flet as ft


# objetivo e adicionar uma habilidade extra ao personagem
def save_new_habilidade(char, habilidade_nome, habilidade_descricao):
    print(habilidade_nome, habilidade_descricao)


def habilidade_imput(char):
    habilidade_nome = ft.TextField(label="Nome")
    habilidade_descricao = ft.TextField(label="Descrição")
    btn_add = ft.IconButton(
        ft.Icons.ADD,
        on_click=save_new_habilidade(
            char, habilidade_nome.value, habilidade_descricao.value
        ),
    )

    habilidade_imput = ft.Column(
        [ft.Row([btn_add, habilidade_nome]), habilidade_descricao]
    )
    return habilidade_imput
