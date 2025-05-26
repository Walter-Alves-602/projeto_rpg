# main.py
from src.infrastructure.adapters.data_files.racas_adapter import RacaFileAdapter
from src.infrastructure.adapters.data_files.classes_adapter import ClasseFileAdapter
from src.application.use_cases.criar_personagem_use_case import CriarPersonagemUseCase
import src.domain.models.armas as armas # Importa o módulo armas da nova localização

if __name__ == "__main__":
    # 1. Adaptadores (Infraestrutura)
    raca_adapter = RacaFileAdapter()
    classe_adapter = ClasseFileAdapter()

    # 2. Casos de Uso (Aplicação)
    criar_personagem_use_case = CriarPersonagemUseCase(raca_repository=raca_adapter, classe_repository=classe_adapter)

    # 3. Interação (Simulando uma interface de usuário)
    try:
        meu_personagem = criar_personagem_use_case.execute(
            nome="Tordek",
            jogador="Você",
            raca_nome="Anão da Colina",
            classe_nome="Barbaro", # Usamos "Barbaro" que tem dados no adapter de classes
            nivel=1,
            forca=15,
            destreza=10,
            constituicao=14,
            inteligencia=8,
            sabedoria=12,
            carisma=9,
        )

        meu_personagem.adicionar_item_inventario(armas.ArcoLongo)
        meu_personagem.adicionar_item_inventario(armas.Adaga)

        print(f"Nome: {meu_personagem.nome}")
        print(f"Jogador: {meu_personagem.jogador}")
        print(f"Raça: {meu_personagem.raca.get('linguas')}")
        print(f"Classe: {meu_personagem.classe.get('dado_de_vida')}")
        print(f"Força Base: {15}") # Valor base para comparação
        print(f"Força Atual: {meu_personagem.atributos['forca']}")
        print(f"Destreza: {meu_personagem.atributos['destreza']}")
        print(f"Constituição Base: {14}") # Valor base para comparação
        print(f"Constituição Atual: {meu_personagem.atributos['constituicao']}")
        print(f"Inventário: {[str(item) for item in meu_personagem.inventario]}")
        print(f"Modificadores de Atributo: {meu_personagem.modificadores_atributo}")
        print(f"Línguas: {meu_personagem.linguas}")
        print(f"Proficiências de Armas (Classe): {meu_personagem.proficiencias_armas}")
        print(f"Proficiências de Armaduras (Classe): {meu_personagem.proficiencias_armaduras}")
        print(f"Testes de Resistência (Classe): {meu_personagem.testes_de_resistencia}")
        print(f"Quantidade de Perícias Escolhíveis (Classe): {meu_personagem.quantidade_de_pericias_classe}")
        print(f"Perícias Disponíveis para Escolha (Classe): {meu_personagem.pericias_disponiveis_para_escolha}")

    except ValueError as e:
        print(f"Erro ao criar personagem: {e}")
