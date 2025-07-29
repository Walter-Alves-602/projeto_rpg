from typing import Dict, Any

ARMAS_DATA: Dict[str, Dict[str, Any]] = {
    "Adaga": {
        "tipo": "corpo_a_corpo",
        "custo": "2 PO",
        "dano": "1d4",
        "tipo_dano": "Perfurante",
        "peso": 0.5,
        "propriedades": ["Leve", "Arremesso (6/18)"],
        "marcial": False,
    },
    "Espada Curta": {
        "tipo": "corpo_a_corpo",
        "custo": "10 PO",
        "dano": "1d6",
        "tipo_dano": "Perfurante",
        "peso": 1.0,
        "propriedades": ["Leve", "Finesse"],
        "marcial": True,
    },
    "Arco Longo": {
        "tipo": "distancia",
        "custo": "50 PO",
        "dano": "1d8",
        "tipo_dano": "Perfurante",
        "peso": 1.0,
        "alcance": "45/180",
        "municao": "Flechas",
        "propriedades": ["Duas Mãos", "Munição"],
        "marcial": True,
    },
    "Besta Leve": {
        "tipo": "distancia",
        "custo": "25 PO",
        "dano": "1d8",
        "tipo_dano": "Perfurante",
        "peso": 2.5,
        "alcance": "24/96",
        "municao": "Virotes",
        "propriedades": ["Recarga", "Duas Mãos", "Munição"],
        "marcial": True,
    },
}