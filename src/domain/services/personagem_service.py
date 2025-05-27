# src/domain/services/personagem_service.py
from src.domain.models.personagem import Personagem
from src.infrastructure.repositories.classe_repository import IClasseRepository # Precisamos dos dados da classe

class PersonagemService:
    def __init__(self, classe_repository: IClasseRepository):
        self._classe_repository = classe_repository

    def calcular_pontos_de_vida_maximos(self, personagem: Personagem) -> int:
        """
        Calcula os pontos de vida máximos de um personagem com base na sua classe e nível.
        """
        classe_data = self._classe_repository.get_classe(personagem.classe_nome)
        if not classe_data:
            raise ValueError(f"Dados da classe '{personagem.classe_nome}' não encontrados.")

        dado_de_vida_str = classe_data.get("dado_de_vida") # Ex: "1d12"
        # Lógica para parsear "1d12" e calcular o HP.
        # Por simplicidade, vamos assumir o valor máximo do dado no primeiro nível e a média nos outros.
        # Nível 1: Max HP do dado + modificador de Constituição
        # Níveis subsequentes: Média do dado (arredondado para cima) + modificador de Constituição

        import re
        match = re.match(r"1d(\d+)", dado_de_vida_str)
        if not match:
            raise ValueError(f"Formato de dado de vida inválido: {dado_de_vida_str}")
        
        dado_de_vida_valor = int(match.group(1))

        # Modificador de Constituição
        mod_con = personagem.modificadores_atributo.get("constituicao", 0)

        hp_max = dado_de_vida_valor + mod_con # HP no Nível 1

        for nivel_atual in range(2, personagem.nivel + 1):
            # Para níveis subsequentes, usa a média + modificador de Constituição
            hp_max += (dado_de_vida_valor // 2) + 1 + mod_con # (Ex: 1d8 = 4 + 1 = 5)

        return hp_max

    def subir_nivel(self, personagem: Personagem) -> None:
        """
        Lógica para subir um personagem de nível.
        """
        personagem.nivel += 1
        # Aqui você chamaria calcular_pontos_de_vida_maximos novamente
        personagem.pontos_de_vida_max = self.calcular_pontos_de_vida_maximos(personagem)
        # Outras lógicas de subida de nível: novos talentos, proficiências, etc.
        print(f"Personagem {personagem.nome} subiu para o nível {personagem.nivel}!")

    # Outros métodos relacionados à lógica do personagem...
    # def escolher_pericias(self, personagem: Personagem, pericias_escolhidas: list) -> None:
    #    ... validações e atribuições ...