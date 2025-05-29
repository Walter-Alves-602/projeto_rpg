# src/infrastructure/adapters/data_files/classes_data.py
from typing import Dict, Any

# Dados estáticos das classes
_CLASSES_DATA: Dict[str, Dict[str, Any]] = {
    "Bárbaro": {
        "dado_de_vida": "1d12",
        "proficiencias_armas": ["Armas simples", "Armas marciais"],
        "proficiencias_armaduras": ["Armadura leve", "Armadura média", "Escudos"],
        "testes_de_resistencia": ["Força", "Constituição"],
        "ferramentas": [],
        "quantidade_de_pericias": 2,
        "pericias_disponiveis": [
            "Adestrar Animais",
            "Atletismo",
            "Intimidação",
            "Natureza",
            "Percepção",
            "Sobrevivência"
        ],
        "habilidades_por_nivel": {
            1: ["Fúria (2 usos)", "Defesa sem Armadura"],
            2: ["Ataque Descuidado", "Percepção de Perigo"],
            3: ["Caminho Primitivo (escolha)", "Fúria (3 usos)"], # Ex: Caminho do Berserker
            4: ["Aumento de Atributo"]
            # ... continue para níveis superiores
        }
    },
    "Bardo": {
        "dado_de_vida": "1d8",
        "proficiencias_armas": ["Armas simples", "Bestas de Mão", "Espadas longas", "Espadas curtas", "Cimitarra"],
        "proficiencias_armaduras": ["Armadura leve"],
        "testes_de_resistencia": ["Destreza", "Carisma"],
        "ferramentas": ["Três instrumentos musicais, à sua escolha"],
        "quantidade_de_pericias": 3,
        "pericias_disponiveis": [
            "Acrobacia", "Adestrar Animais", "Arcanismo", "Atletismo", "Atuação",
            "Enganação", "Furtividade", "História", "Intimidação", "Intuição",
            "Investigação", "Lidar com Animais", "Medicina", "Natureza", "Percepção",
            "Persuasão", "Prestidigitação", "Religião", "Sobrevivência"
        ],
        "habilidades_por_nivel": {
            1: ["Conjuração", "Inspiração Bárdica (d6, 3 usos)", "Magias (Lista inicial)"], # Referência a magias
            2: ["Canção de Descanso (1d6)", "Jack of All Trades", "Song of Rest"],
            3: ["Especialidade (escolha)", "Proficiência Adicional"], # Ex: Colégio do Conhecimento
            4: ["Aumento de Atributo"]
            # ... continue para níveis superiores
        }
    },
    # --- NOVAS CLASSES AQUI ---
    "Clérigo": {
        "dado_de_vida": "1d8",
        "proficiencias_armas": ["Armas simples"],
        "proficiencias_armaduras": ["Armadura leve", "Armadura média", "Escudos"],
        "testes_de_resistencia": ["Sabedoria", "Carisma"],
        "ferramentas": [],
        "quantidade_de_pericias": 2,
        "pericias_disponiveis": [
            "História", "Intuição", "Medicina", "Persuasão", "Religião"
        ],
        "habilidades_por_nivel": {
            1: ["Conjuração (Clérigo)", "Discípulo da Vida (ou outro domínio)", "Domínio Divino (escolha)"],
            2: ["Canalizar Divindade (1 uso)", "Expulsar Mortos-Vivos"],
            3: ["Magias de Domínio Adicionais"],
            4: ["Aumento de Atributo"]
            # ...
        }
    },
    "Guerreiro": {
        "dado_de_vida": "1d10",
        "proficiencias_armas": ["Armas simples", "Armas marciais"],
        "proficiencias_armaduras": ["Todas as armaduras", "Escudos"],
        "testes_de_resistencia": ["Força", "Constituição"],
        "ferramentas": [],
        "quantidade_de_pericias": 2,
        "pericias_disponiveis": [
            "Acrobacia", "Adestrar Animais", "Atletismo", "História",
            "Intimidação", "Intuição", "Percepção", "Sobrevivência"
        ],
        "habilidades_por_nivel": {
            1: ["Estilo de Luta (escolha)", "Recuperar Fôlego (1 uso)"],
            2: ["Ação de Batalha (1 uso)"],
            3: ["Arquétipo Marcial (escolha)"], # Ex: Mestre de Batalha, Campeão
            4: ["Aumento de Atributo"]
            # ...
        }
    },
    "Mago": {
        "dado_de_vida": "1d6",
        "proficiencias_armas": ["Adagas", "Fundas", "Bestas leves", "Bordões", "Dardos"],
        "proficiencias_armaduras": [],
        "testes_de_resistencia": ["Inteligência", "Sabedoria"],
        "ferramentas": [],
        "quantidade_de_pericias": 2,
        "pericias_disponiveis": [
            "Arcanismo", "História", "Intuição", "Investigação", "Medicina", "Religião"
        ],
        "habilidades_por_nivel": {
            1: ["Conjuração (Mago)", "Recuperação Arcana", "Livro de Magias"],
            2: ["Tradição Arcana (escolha)", "Magias de Tradição"], # Ex: Escola de Evocação
            3: ["Magias de Nível 2"],
            4: ["Aumento de Atributo"]
            # ...
        }
    },
    "Ladino": {
        "dado_de_vida": "1d8",
        "proficiencias_armas": ["Armas simples", "Bestas de mão", "Espadas longas", "Espadas curtas", "Cimitarra"],
        "proficiencias_armaduras": ["Armadura leve"],
        "testes_de_resistencia": ["Destreza", "Inteligência"],
        "ferramentas": ["Ferramentas de ladrão"],
        "quantidade_de_pericias": 4,
        "pericias_disponiveis": [
            "Acrobacia", "Atletismo", "Atuação", "Enganação", "Furtividade",
            "Intimidação", "Intuição", "Investigação", "Percepção", "Persuasão",
            "Prestidigitação"
        ],
        "habilidades_por_nivel": {
            1: ["Perícia (4 perícias, 2 proficiências extras)", "Ataque Furtivo (1d6)", "Gíria de Ladrão"],
            2: ["Ação Astuta"],
            3: ["Arquétipo Ladino (escolha)"], # Ex: Ladrão, Assassino
            4: ["Aumento de Atributo"]
            # ...
        }
    }
    # Adicione mais classes aqui conforme necessário (Feiticeiro, Paladino, Monge, Druida, Patrulheiro, Bruxo)
}