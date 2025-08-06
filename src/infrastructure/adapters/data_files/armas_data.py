from typing import Any, Dict

ARMAS_DATA: Dict[str, Dict[str, Any]] = {
    # Armas Simples Corpo-a-Corpo
    "Adaga": {
        "tipo": "corpo_a_corpo",
        "custo": "2 PO",
        "dano": "1d4",
        "tipo_dano": "Perfurante",
        "peso": 0.5,
        "propriedades": ["acuidade","Leve", "Arremesso (6/18)"],
        "marcial": False
    },
    "Azagaia": {
        "tipo": "corpo_a_corpo",
        "custo": "5 PP",
        "dano": "1d6",
        "tipo_dano": "Perfurante",
        "peso": 1.0,
        "propriedades": ["Arremesso (9/36)"],
        "marcial": False
    },
    "Bordão": {
        "tipo": "corpo_a_corpo",
        "custo": "2 PP",
        "dano": "1d6",
        "tipo_dano": "Concussão",
        "peso": 2.0,
        "propriedades": ["Versátil (1d8)"],
        "marcial": False
    },
    "Clava Grande": {
        "tipo": "corpo_a_corpo",
        "custo": "2 PP",
        "dano": "1d8",
        "tipo_dano": "Concussão",
        "peso": 5.0,
        "propriedades": ["Pesada", "Duas Mãos"],
        "marcial": False
    },
    "Foice Curta": {
        "tipo": "corpo_a_corpo",
        "custo": "1 PO",
        "dano": "1d4",
        "tipo_dano": "Cortante",
        "peso": 1.0,
        "propriedades": ["Leve"],
        "marcial": False
    },
    "Lança": {
        "tipo": "corpo_a_corpo",
        "custo": "1 PO",
        "dano": "1d6",
        "tipo_dano": "Perfurante",
        "peso": 1.5,
        "propriedades": ["Arremesso (6/18)", "Versátil (1d8)"],
        "marcial": False
    },
    "Maça": {
        "tipo": "corpo_a_corpo",
        "custo": "5 PO",
        "dano": "1d6",
        "tipo_dano": "Concussão",
        "peso": 2.0,
        "propriedades": [],
        "marcial": False
    },
    "Machadinha": {
        "tipo": "corpo_a_corpo",
        "custo": "5 PO",
        "dano": "1d6",
        "tipo_dano": "Cortante",
        "peso": 1.0,
        "propriedades": ["Leve", "Arremesso (6/18)"],
        "marcial": False
    },
    "Martelo Leve": {
        "tipo": "corpo_a_corpo",
        "custo": "2 PO",
        "dano": "1d4",
        "tipo_dano": "Concussão",
        "peso": 1.0,
        "propriedades": ["Leve", "Arremesso (6/18)"],
        "marcial": False
    },
    "Porrete": {
        "tipo": "corpo_a_corpo",
        "custo": "1 PP",
        "dano": "1d4",
        "tipo_dano": "Concussão",
        "peso": 1.0,
        "propriedades": ["Leve"],
        "marcial": False
    },
    # Armas Simples à Distância
    "Arco Curto": {
        "tipo": "distancia",
        "custo": "25 PO",
        "dano": "1d6",
        "tipo_dano": "Perfurante",
        "peso": 1.0,
        "propriedades": ["Munição (24/96)", "Duas Mãos"],
        "marcial": False
    },
    "Beste Leve": {
        "tipo": "distancia",
        "custo": "25 PO",
        "dano": "1d8",
        "tipo_dano": "Perfurante",
        "peso": 2.5,
        "propriedades": ["Munição (24/96)", "Recarga", "Duas Mãos"],
        "marcial": False
    },
    "Dardo": {
        "tipo": "distancia",
        "custo": "5 PC",
        "dano": "1d4",
        "tipo_dano": "Perfurante",
        "peso": 0.1,
        "propriedades": ["acuidade", "Arremesso (6/18)"],
        "marcial": False
    },
    "Funda": {
        "tipo": "distancia",
        "custo": "1 PP",
        "dano": "1d4",
        "tipo_dano": "Concussão",
        "peso": 0.0,
        "propriedades": ["Munição (9/36)"],
        "marcial": False
    },
    # Armas Marciais Corpo-a-Corpo
    "Alabarda": {
        "tipo": "corpo_a_corpo",
        "custo": "20 PO",
        "dano": "1d10",
        "tipo_dano": "Cortante",
        "peso": 3.0,
        "propriedades": ["Pesada", "Alcance", "Duas Mãos"],
        "marcial": True
    },
    "Cimitarra": {
        "tipo": "corpo_a_corpo",
        "custo": "25 PO",
        "dano": "1d6",
        "tipo_dano": "Cortante",
        "peso": 1.5,
        "propriedades": ["acuidade", "Leve"],
        "marcial": True
    },
    "Chicote": {
        "tipo": "corpo_a_corpo",
        "custo": "2 PO",
        "dano": "1d4",
        "tipo_dano": "Cortante",
        "peso": 1.5,
        "propriedades": ["acuidade", "Alcance"],
        "marcial": True
    },
    "Espada Curta": {
        "tipo": "corpo_a_corpo",
        "custo": "10 PO",
        "dano": "1d6",
        "tipo_dano": "Perfurante",
        "peso": 1.0,
        "propriedades": ["acuidade", "Leve"],
        "marcial": True
    },
    "Espada Grande": {
        "tipo": "corpo_a_corpo",
        "custo": "50 PO",
        "dano": "2d6",
        "tipo_dano": "Cortante",
        "peso": 3.0,
        "propriedades": ["Pesada", "Duas Mãos"],
        "marcial": True
    },
    "Espada Longa": {
        "tipo": "corpo_a_corpo",
        "custo": "15 PO",
        "dano": "1d8",
        "tipo_dano": "Cortante",
        "peso": 1.5,
        "propriedades": ["Versátil (1d10)"],
        "marcial": True
    },
    "Glaive": {
        "tipo": "corpo_a_corpo",
        "custo": "20 PO",
        "dano": "1d10",
        "tipo_dano": "Cortante",
        "peso": 3.0,
        "propriedades": ["Pesada", "Alcance", "Duas Mãos"],
        "marcial": True
    },
    "Lança de Montaria": {
        "tipo": "corpo_a_corpo",
        "custo": "10 PO",
        "dano": "1d12",
        "tipo_dano": "Perfurante",
        "peso": 3.0,
        "propriedades": ["Alcance", "Especial"],
        "marcial": True
    },
    "Lança Longa": {
        "tipo": "corpo_a_corpo",
        "custo": "5 PO",
        "dano": "1d10",
        "tipo_dano": "Perfurante",
        "peso": 4.0,
        "propriedades": ["Pesada", "Alcance", "Duas Mãos"],
        "marcial": True
    },
    "Maça Estrela": {
        "tipo": "corpo_a_corpo",
        "custo": "15 PO",
        "dano": "1d8",
        "tipo_dano": "Perfurante",
        "peso": 2.0,
        "propriedades": [],
        "marcial": True
    },
    "Machado Grande": {
        "tipo": "corpo_a_corpo",
        "custo": "30 PO",
        "dano": "1d12",
        "tipo_dano": "Cortante",
        "peso": 3.5,
        "propriedades": ["Pesada", "Duas Mãos"],
        "marcial": True
    },
    "Machado de Batalha": {
        "tipo": "corpo_a_corpo",
        "custo": "10 PO",
        "dano": "1d8",
        "tipo_dano": "Cortante",
        "peso": 2.0,
        "propriedades": ["Versátil (1d10)"],
        "marcial": True
    },
    "Malho": {
        "tipo": "corpo_a_corpo",
        "custo": "10 PO",
        "dano": "2d6",
        "tipo_dano": "Concussão",
        "peso": 5.0,
        "propriedades": ["Pesada", "Duas Mãos"],
        "marcial": True
    },
    "Mangual": {
        "tipo": "corpo_a_corpo",
        "custo": "10 PO",
        "dano": "1d8",
        "tipo_dano": "Concussão",
        "peso": 1.0,
        "propriedades": [],
        "marcial": True
    },
    "Martelo de Guerra": {
        "tipo": "corpo_a_corpo",
        "custo": "15 PO",
        "dano": "1d8",
        "tipo_dano": "Concussão",
        "peso": 1.0,
        "propriedades": ["Versátil (1d10)"],
        "marcial": True
    },
    "Picareta de Guerra": {
        "tipo": "corpo_a_corpo",
        "custo": "5 PO",
        "dano": "1d8",
        "tipo_dano": "Perfurante",
        "peso": 1.0,
        "propriedades": [],
        "marcial": True
    },
    "Rapieira": {
        "tipo": "corpo_a_corpo",
        "custo": "25 PO",
        "dano": "1d8",
        "tipo_dano": "Perfurante",
        "peso": 1.0,
        "propriedades": ["acuidade"],
        "marcial": True
    },
    "Tridente": {
        "tipo": "corpo_a_corpo",
        "custo": "5 PO",
        "dano": "1d6",
        "tipo_dano": "Perfurante",
        "peso": 2.0,
        "propriedades": ["Arremesso (6/18)", "Versátil (1d8)"],
        "marcial": True
    },
    #Armas Marciais à Distância
    "Arco Longo": {
        "tipo": "distancia",
        "custo": "50 PO",
        "dano": "1d8",
        "tipo_dano": "Perfurante",
        "peso": 1.0,
        "propriedades": ["Munição (45/180)", "Pesada", "Duas Mãos"],
        "marcial": True
    },
    "Besta de Mão": {
        "tipo": "distancia",
        "custo": "75 PO",
        "dano": "1d6",
        "tipo_dano": "Perfurante",
        "peso": 1.5,
        "propriedades": ["Munição (9/36)", "Leve", "Recarga"],
        "marcial": True
    },
    "Besta Pesada": {
        "tipo": "distancia",
        "custo": "50 PO",
        "dano": "1d10",
        "tipo_dano": "Perfurante",
        "peso": 4.5,
        "propriedades": ["Munição (30/120)", "Pesada", "Recarga", "Duas Mãos"],
        "marcial": True
    },
    "Rede": {
        "tipo": "distancia",
        "custo": "1 PO",
        "dano": "",
        "tipo_dano": "",
        "peso": 1.5,
        "propriedades": ["Especial", "Arremesso (1.5/4.5)"],
        "marcial": True
    },
    "Zarabatana": {
        "tipo": "distancia",
        "custo": "10 PO",
        "dano": "1",
        "tipo_dano": "Perfurante",
        "peso": 0.5,
        "propriedades": ["Munição (7.5/30)", "Recarga"],
        "marcial": True
    }
}
