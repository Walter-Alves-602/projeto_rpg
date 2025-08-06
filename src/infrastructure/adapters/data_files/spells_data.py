from typing import Any, Dict

_SPELLS_DATA: Dict[str, Dict[str, Any]] = {
    "Ataque Certeiro": {
        "nivel": 0,  # Magias de nível 0 são truques (cantrips)
        "escola": "Adivinhação",
        "tempo_conjuracao": "1 ação",
        "alcance": "30 pés",
        "componentes": ["V", "S"], # V: Verbal, S: Somático, M: Material
        "duracao": "Até o final do seu próximo turno",
        "descricao": "Você estende sua mão e aponta o dedo para um alvo à vista dentro do alcance. Seus olhos se arregalam, o que te dá uma breve percepção mística da vulnerabilidade do seu alvo. No seu próximo turno, você tem vantagem na primeira jogada de ataque que você fizer contra este alvo. Você não tem vantagem de ataques subsequentes contra o alvo neste turno.",
        "classes": ["Bardo", "Bruxo", "Feiticeiro", "Mago"],
        "detalhes_em_niveis_superiores": None
    },
    "Bênção": {
        "nivel": 1,
        "escola": "Encantamento",
        "tempo_conjuracao": "1 ação",
        "alcance": "30 pés",
        "componentes": ["V", "S", "M (um aspersor de água benta ou pó de prata sagrada)"],
        "duracao": "Concentração, até 1 minuto",
        "descricao": "Você toca até três criaturas à sua escolha dentro do alcance. Toda vez que um alvo realizar uma jogada de ataque ou um teste de resistência antes da magia terminar, o alvo pode jogar 1d4 e adicionar o número rolado ao total da jogada de ataque ou teste de resistência.",
        "detalhes_em_niveis_superiores": {
            "regra": "Para cada nível de magia acima do 1º, você pode afetar uma criatura adicional.",
            "exemplo": "Nível 2: afeta 4 criaturas; Nível 3: afeta 5 criaturas."
        },
        "classes": ["Clérigo", "Paladino"]
    },
    "Bola de Fogo": {
        "nivel": 3,
        "escola": "Evocação",
        "tempo_conjuracao": "1 ação",
        "alcance": "150 pés",
        "componentes": ["V", "S", "M (uma pequena bola de guano de morcego e enxofre)"],
        "duracao": "Instantâneo",
        "descricao": "Uma labareda de fogo irrompe do seu dedo, estendendo-se para um ponto escolhido dentro do alcance. Cada criatura em uma esfera de 20 pés de raio centrada naquele ponto deve fazer um teste de resistência de Destreza. Uma criatura sofre 8d6 de dano de fogo se falhar na resistência, ou metade desse dano se obtiver sucesso.",
        "detalhes_em_niveis_superiores": {
            "regra": "Quando você conjura esta magia usando um espaço de magia de 4º nível ou superior, o dano aumenta em 1d6 para cada nível de magia acima do 3º.",
            "exemplo": "Nível 4: 9d6 de dano; Nível 5: 10d6 de dano."
        },
        "classes": ["Feiticeiro", "Mago"]
    },
    "Curar Ferimentos": {
        "nivel": 1,
        "escola": "Evocação",
        "tempo_conjuracao": "1 ação",
        "alcance": "Toque",
        "componentes": ["V", "S"],
        "duracao": "Instantâneo",
        "descricao": "Uma criatura que você toca recupera uma quantidade de pontos de vida igual a 1d8 + seu modificador de atributo de conjuração. Esta magia não tem efeito em mortos-vivos ou constructos.",
        "detalhes_em_niveis_superiores": {
            "regra": "Quando você conjura esta magia usando um espaço de magia de 2º nível ou superior, a cura aumenta em 1d8 para cada nível de magia acima do 1º.",
            "exemplo": "Nível 2: 2d8 + modificador; Nível 3: 3d8 + modificador."
        },
        "classes": ["Bardo", "Clérigo", "Druida", "Paladino", "Guardião"]
    },
    "Mísseis Mágicos": {
        "nivel": 1,
        "escola": "Evocação",
        "tempo_conjuracao": "1 ação",
        "alcance": "120 pés",
        "componentes": ["V", "S"],
        "duracao": "Instantâneo",
        "descricao": "Você cria três dardos brilhantes de força mágica. Cada dardo atinge uma criatura à sua escolha que você possa ver dentro do alcance. Um dardo causa 1d4 + 1 de dano de força ao alvo. Os dardos atingem simultaneamente e você pode direcioná-los para uma criatura ou várias.",
        "detalhes_em_niveis_superiores": {
            "regra": "Quando você conjura esta magia usando um espaço de magia de 2º nível ou superior, a magia cria um dardo adicional para cada nível de magia acima do 1º.",
            "exemplo": "Nível 2: 4 dardos; Nível 3: 5 dardos."
        },
        "classes": ["Feiticeiro", "Mago"]
    }
}