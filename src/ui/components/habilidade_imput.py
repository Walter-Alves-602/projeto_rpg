from typing import Callable

import flet as ft


def habilidade_imput(on_add: Callable[[str, str], None]):
    """
    Componente de UI para adicionar uma nova habilidade.
    Recebe uma função de callback 'on_add' que é chamada quando o botão é clicado.
    """
    habilidade_nome = ft.TextField(label="Nome")
    habilidade_descricao = ft.TextField(label="Descrição")
    btn_add = ft.IconButton(
        ft.Icons.ADD,
        on_click=lambda _: on_add(
            habilidade_nome.value, habilidade_descricao.value
        ),
    )

    habilidade_imput_element = ft.Column(
        [ft.Row([btn_add, habilidade_nome]), habilidade_descricao]
    )
    return habilidade_imput_element
