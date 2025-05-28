# main.py
from src.infrastructure.adapters.data_files.racas_adapter import RacaFileAdapter
from src.infrastructure.adapters.data_files.classes_adapter import ClasseFileAdapter
from src.application.use_cases.criar_personagem_use_case import CriarPersonagemUseCase
from src.application.use_cases.gerenciar_personagem_use_case import GerenciarPersonagemUseCase
from src.infrastructure.adapters.database.sqlite_character_repository import SQLitePersonagemRepository
from src.persistence.database_manager import DatabaseManager
import src.domain.models.armas as armas

if __name__ == "__main__":
    # 0. Inicializar o banco de dados
    db_manager = DatabaseManager()
    db_manager.create_tables() # Garante que as tabelas existem

    # 1. Adaptadores de Dados (arquivos estáticos)
    raca_file_adapter = RacaFileAdapter()
    classe_file_adapter = ClasseFileAdapter()

    # 2. Adaptador de Persistência (Banco de Dados)
    # Note que o repositório de Personagem precisa dos outros repositórios
    # para poder reconstruir o objeto Personagem com as dependências corretas.
    personagem_db_repository = SQLitePersonagemRepository(
        db_manager=db_manager,
        raca_repository=raca_file_adapter, # Usamos o adaptador de arquivo para raças/classes aqui
        classe_repository=classe_file_adapter
    )

    # 3. Casos de Uso (Aplicação)
    criar_personagem_uc = CriarPersonagemUseCase(
        raca_repository=raca_file_adapter,
        classe_repository=classe_file_adapter
    )
    gerenciar_personagem_uc = GerenciarPersonagemUseCase(
        personagem_repository=personagem_db_repository
    )

    # --- Fluxo de Exemplo ---

    print("--- Tentando carregar personagens existentes ---")
    personagens_existentes = gerenciar_personagem_uc.listar_todos_personagens()

    print("\n--- Criando um novo personagem ---")
    try:
        novo_personagem = criar_personagem_uc.execute(
            nome="Elara",
            jogador="Jogador Teste",
            raca_nome="Elfo Alto",
            classe_nome="Bardo", # Bardo está definido no classes_adapter
            nivel=1,
            forca=10,
            destreza=14,
            constituicao=12,
            inteligencia=15,
            sabedoria=13,
            carisma=16,
        )
        print(f"Personagem '{novo_personagem.nome}' criado em memória.")
        print(f"Atributos da Elara (com bônus de raça): {novo_personagem.atributos}")
        print(f"Proficiências de Armas (Classe): {novo_personagem.proficiencias_armas}")
        print(f"Perícias Disponíveis para Escolha (Classe): {novo_personagem.pericias_disponiveis_para_escolha}")

        # Salvar o novo personagem no banco de dados
        gerenciar_personagem_uc.salvar_personagem(novo_personagem)

    except ValueError as e:
        print(f"Erro ao criar personagem: {e}")

    print("\n--- Carregando o personagem 'Elara' do banco de dados ---")
    personagem_carregado = gerenciar_personagem_uc.carregar_personagem("Elara")

    if personagem_carregado:
        print(f"Personagem Carregado: {personagem_carregado.nome}")
        print(f"Raça do Carregado: {personagem_carregado.raca.get('nome', personagem_carregado.raca_nome)}")
        print(f"Classe do Carregado: {personagem_carregado.classe.get('nome', personagem_carregado.classe_nome)}")
        print(f"Atributos do Carregado: {personagem_carregado.atributos}")
        print(f"Modificadores de Atributo do Carregado: {personagem_carregado.modificadores_atributo}")
        print(f"Línguas do Carregado: {personagem_carregado.linguas}")
        print(f"Proficiências de Armas (Carregado): {personagem_carregado.proficiencias_armas}")

    print("\n--- Tentando listar todos os personagens novamente ---")
    gerenciar_personagem_uc.listar_todos_personagens()

    print("\n--- Deletando o personagem 'Elara' ---")
    gerenciar_personagem_uc.deletar_personagem("Elara")

    print("\n--- Listando todos os personagens após a exclusão ---")
    gerenciar_personagem_uc.listar_todos_personagens()