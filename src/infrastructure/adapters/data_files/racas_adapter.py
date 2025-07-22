from src.infrastructure.repositories import IRacaRepository

_RACA_DATA = {
    "Anão": {
        "atributos": {"constituicao": 2},
        "linguas": ["Comum", "Anão"],
        "deslocamento": 7.5,
        "habilidades_raciais": [
            "Visão no Escuro",
            "Resistência Anã",
            "Proficiência em Ferramentas Anãs",
        ],
    },
    "Anão da Colina": {
        "atributos": {"constituicao": 2, "sabedoria": 1},
        "linguas": ["Comum", "Anão"],
        "deslocamento": 7.5,
        "habilidades_raciais": [
            "Visão no Escuro",
            "Resistência Anã",
            "Proficiência em Ferramentas Anãs",
            "Especialização em Pedra",
        ]
    },
    "Anão da Montanha": {
        "atributos": {"forca": 2, "constituicao": 2},
        "linguas": ["Comum", "Anão"],
        "deslocamento": 7.5,
        "habilidades_raciais": [
            "Visão no Escuro",
            "Resistência Anã",
            "Proficiência em Ferramentas Anãs",
            "Treinamento em Combate Anão",
        ],
    },
    "Elfo": {
        "atributos": {"destreza": 2},
        "linguas": ["Comum", "Elfico"],
        "deslocamento": 9,
        "habilidades_raciais": ["Visão no Escuro", "Ancestralidade Feérica", "Transe"],
    },
    "Elfo Alto": {
        "atributos": {"inteligencia": 1, "destreza": 2},
        "linguas": ["Comum", "Elfico"],
        "deslocamento": 9,
        "habilidades_raciais": [
            "Visão no Escuro",
            "Ancestralidade Feérica",
            "Transe",
            "Treinamento com Armas Élficas",
            "Magia Alta Élfica",
            "Escrita Élfica",
        ],
    },
    "Elfo da Floresta": {
        "atributos": {"destreza": 2, "sabedoria": 1},
        "linguas": ["Comum", "Elfico"],
        "deslocamento": 9,
        "habilidades_raciais": [
            "Visão no Escuro",
            "Ancestralidade Feérica",
            "Transe",
            "Treinamento com Armas do Elfo da Floresta",
            "Pés Ligeiros",
            "Máscara da Natureza",
        ],
    },
    "Elfo Negro": {
        "atributos": {"carisma": 1, "destreza": 2},
        "linguas": ["Comum", "Elfico", "Subterrâneo"],
        "deslocamento": 9,
        "habilidades_raciais": [
            "Visão no Escuro Superior",
            "Ancestralidade Feérica",
            "Transe",
            "Magia Drow",
            "Armamento Drow",
            "Sensibilidade à Luz Solar",
        ],
    },
    "Halfling": {
        "atributos": {"destreza": 2},
        "linguas": ["Comum", "Halfling"],
        "deslocamento": 7.5,
        "habilidades_raciais": ["Coragem Halfling", "Agilidade Halfling"],
    },
    "Halfling Pés Leves": {
        "atributos": {"carisma": 1, "destreza": 2},
        "linguas": ["Comum", "Halfling"],
        "deslocamento": 7.5,
        "habilidades_raciais": ["Coragem Halfling", "Agilidade Halfling"],
    },
    "Halfling Robusto": {
        "atributos": {"forca": 1, "destreza": 2},
        "linguas": ["Comum", "Halfling"],
        "deslocamento": 7.5,
        "habilidades_raciais": [
            "Coragem Halfling",
            "Agilidade Halfling",
            "Fortitude Robusta",
        ],
    },
    "Humano": {
        "atributos": {
            "forca": 1,
            "destreza": 1,
            "constituicao": 1,
            "inteligencia": 1,
            "sabedoria": 1,
            "carisma": 1,
        },
        "linguas": ["Comum"],
        "deslocamento": 9,
        "habilidades_raciais": ["Idiomas Adicionais"],
    },
    "Draconato": {
        "atributos": {"forca": 2, "carisma": 1},
        "linguas": ["Comum", "Dracônico"],
        "deslocamento": 9,
        "habilidades_raciais": [
            "Ancestral Dracônica",
            "Resistência a Dano Dracônico",
            "Sopro Dracônico",
        ],
    },
    "Gnomo": {
        "atributos": {"inteligencia": 2},
        "linguas": ["Comum", "Gnômico"],
        "deslocamento": 7.5,
        "habilidades_raciais": ["Visão no Escuro", "Astúcia Gnômica"],
    },
    "Gnomo da Floresta": {
        "atributos": {"inteligencia": 2, "destreza": 1},
        "linguas": ["Comum", "Gnômico"],
        "deslocamento": 7.5,
        "habilidades_raciais": ["Visão no Escuro", "Astúcia Gnômica", "Ilusão Menor"],
    },
    "Gnomo da Rocha": {
        "atributos": {"inteligencia": 2, "constituicao": 1},
        "linguas": ["Comum", "Gnômico"],
        "deslocamento": 7.5,
        "habilidades_raciais": [
            "Visão no Escuro",
            "Astúcia Gnômica",
            "Construtor de Gnomo da Rocha",
            "Engenhoso",
        ],
    },
    "Meio-Elfo": {
        "atributos": {
            "carisma": 2,
            "destreza": 1,
        },  # Destreza ou outro atributo é a escolha do jogador
        "linguas": ["Comum", "Élfico"],  # +1 idioma extra
        "deslocamento": 9,
        "quantidade_de_atributos_escolha": 1,  # Indica que 2 atributos aumentam em 1 (já 1 do carisma, precisa de +1)
        "habilidades_raciais": [
            "Visão no Escuro",
            "Ancestralidade Feérica",
            "Habilidades Versáteis",
            "Idiomas Adicionais",
        ],  # Habilidades Versáteis lida com as perícias e idiomas
    },
    "Meio-Orc": {
        "atributos": {"forca": 2, "constituicao": 1},
        "linguas": ["Comum", "Orc"],
        "deslocamento": 9,
        "habilidades_raciais": [
            "Visão no Escuro",
            "Ameaça Intimidadora",
            "Resistência Implacável",
            "Ataques Selvagens",
        ],
    },
    "Tiefling": {
        "atributos": {"inteligencia": 1, "carisma": 2},
        "linguas": ["Comum", "Infernal"],
        "deslocamento": 9,
        "habilidades_raciais": [
            "Visão no Escuro",
            "Herança Infernal",
            "Resistência ao Fogo",
        ],
    },
}


class RacaFileAdapter(IRacaRepository):
    def get_raca(self, nome_raca: str) -> dict:
        """
        Retorna os dados de uma raça do arquivo de dados.
        """
        return _RACA_DATA.get(nome_raca, {})

    def get_all_raca_names(self):
        return list(_RACA_DATA.keys())
