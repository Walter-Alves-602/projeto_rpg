import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.persistence.database_manager import DatabaseManager
from src.infrastructure.adapters.database.sqlite_character_repository import SQLitePersonagemRepository
from src.infrastructure.adapters.data_files.racas_adapter import RacaFileAdapter
from src.infrastructure.adapters.data_files.classes_adapter import ClasseFileAdapter
from src.infrastructure.adapters.data_files.habilidades_raciais_file_adapter import HabilidadesRaciaisFileAdapter
from src.infrastructure.adapters.data_files.spells_file_adapter import SpellFileAdapter
from src.application.use_cases.gerenciar_personagem_use_case import GerenciarPersonagemUseCase

def terminal_ui():
    db_manager = DatabaseManager()
    db_manager.create_tables()  # Garante que as tabelas existem

    raca_repository = RacaFileAdapter()
    classe_repository = ClasseFileAdapter()
    habilidades_raciais_repository = HabilidadesRaciaisFileAdapter()
    spell_repository = SpellFileAdapter()

    personagem_repository = SQLitePersonagemRepository(
        db_manager,
        raca_repository,
        classe_repository,
        habilidades_raciais_repository
    )

    gerenciar_personagem_uc = GerenciarPersonagemUseCase(
        personagem_repository,
        raca_repository,
        classe_repository,
        habilidades_raciais_repository,
        spell_repository
    )

    while True:
        print("\n--- Menu Principal ---")
        print("1. Criar novo personagem")
        print("2. Ver todos os personagens")
        print("3. Ver detalhes de um personagem")
        print("4. Excluir personagem")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            print("\n--- Criar Novo Personagem ---")
            nome = input("Nome do Personagem: ")
            jogador = input("Nome do Jogador: ")

            # Listar raças disponíveis
            print("\nRaças disponíveis:")
            racas_disponiveis = raca_repository.get_all_raca_names()
            for i, r in enumerate(racas_disponiveis):
                print(f"{i+1}. {r}")
            raca_escolhida_idx = int(input(f"Escolha a raça (1-{len(racas_disponiveis)}): ")) - 1
            raca_nome = racas_disponiveis[raca_escolhida_idx]

            # Listar classes disponíveis
            print("\nClasses disponíveis:")
            classes_disponiveis = classe_repository.get_all_classe_names()
            for i, c in enumerate(classes_disponiveis):
                print(f"{i+1}. {c}")
            classe_escolhida_idx = int(input(f"Escolha a classe (1-{len(classes_disponiveis)}): ")) - 1
            classe_nome = classes_disponiveis[classe_escolhida_idx]

            # Atributos básicos
            print("\nAtributos (pontos):")
            forca = int(input("Força: "))
            destreza = int(input("Destreza: "))
            constituicao = int(input("Constituição: "))
            inteligencia = int(input("Inteligência: "))
            sabedoria = int(input("Sabedoria: "))
            carisma = int(input("Carisma: "))

            try:
                novo_personagem = gerenciar_personagem_uc.criar_personagem(
                    nome=nome,
                    jogador=jogador,
                    raca_nome=raca_nome,
                    classe_nome=classe_nome,
                    nivel=1, # Nível inicial
                    forca=forca,
                    destreza=destreza,
                    constituicao=constituicao,
                    inteligencia=inteligencia,
                    sabedoria=sabedoria,
                    carisma=carisma
                )
                print(f"\nPersonagem '{novo_personagem.nome}' criado com sucesso!")

                print("\nHabilidades Raciais:")
                habilidades_detalhadas = novo_personagem.get_habilidades_raciais_com_descricao(habilidades_raciais_repository)
                if habilidades_detalhadas:
                    for habilidade in habilidades_detalhadas:
                        print(f"- {habilidade['nome']}: {habilidade['descricao']}")
                else:
                    print("Nenhuma habilidade racial para esta raça.")

                print("\nMagias da Classe:")
                magias_da_classe = spell_repository.get_spells_by_class(novo_personagem.classe_nome)
                if magias_da_classe:
                    for magia in magias_da_classe:
                        print(f"- {magia['nome']} (Nível {magia['nivel']}, Escola: {magia['escola']})")
                else:
                    print(f"Nenhuma magia para a classe {novo_personagem.classe_nome}.")

            except ValueError as e:
                print(f"Erro ao criar personagem: {e}")

        elif escolha == '2':
            print("\n--- Todos os Personagens ---")
            personagens_existentes = gerenciar_personagem_uc.listar_todos_personagens()
            if not personagens_existentes:
                print("Nenhum personagem cadastrado.")
            else:
                for p in personagens_existentes:
                    print(f"- {p.nome} (Raça: {p.raca_nome}, Classe: {p.classe_nome}, Nível: {p.nivel})")

        elif escolha == '3':
            print("\n--- Detalhes do Personagem ---")
            nome_busca = input("Digite o nome do personagem para ver os detalhes: ")
            personagem = gerenciar_personagem_uc.obter_personagem_por_nome(nome_busca)
            if personagem:
                print(f"\nNome: {personagem.nome}")
                print(f"Jogador: {personagem.jogador}")
                print(f"Raça: {personagem.raca_nome}")
                print(f"Classe: {personagem.classe_nome}")
                print(f"Nível: {personagem.nivel}")
                print(f"PV: {personagem.pontos_de_vida_atual}/{personagem.pontos_de_vida_max}")
                print(f"Deslocamento: {personagem.deslocamento} metros")
                print("\nAtributos:")
                for attr, val in personagem.atributos.items():
                    mod = personagem.modificadores_atributo[attr]
                    print(f"  {attr.capitalize()}: {val} (Mod: {'+' if mod >= 0 else ''}{mod})")

                print("\nHabilidades Raciais:")
                habilidades_detalhadas = personagem.get_habilidades_raciais_com_descricao(habilidades_raciais_repository)
                if habilidades_detalhadas:
                    for habilidade in habilidades_detalhadas:
                        print(f"- {habilidade['nome']}: {habilidade['descricao']}")
                else:
                    print("Nenhuma habilidade racial para esta raça.")

                print("\nMagias da Classe:")
                magias_da_classe = spell_repository.get_spells_by_class(personagem.classe_nome)
                if magias_da_classe:
                    for magia in magias_da_classe:
                        print(f"- {magia['nome']} (Nível {magia['nivel']}, Escola: {magia['escola']})")
                else:
                    print(f"Nenhuma magia para a classe {personagem.classe_nome}.")

            else:
                print(f"Personagem '{nome_busca}' não encontrado.")

        elif escolha == '4':
            print("\n--- Excluir Personagem ---")
            nome_excluir = input("Digite o nome do personagem a ser excluído: ")
            try:
                gerenciar_personagem_uc.excluir_personagem(nome_excluir)
                print(f"Personagem '{nome_excluir}' excluído com sucesso.")
            except ValueError as e:
                print(f"Erro ao excluir personagem: {e}")

        elif escolha == '5':
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")


if __name__ == "__main__":
    terminal_ui()