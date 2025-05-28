# src/persistence/database_manager.py
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="rpg_ficha.db"):
        # Garante que a pasta 'data' exista para armazenar o DB
        self.db_folder = "data"
        os.makedirs(self.db_folder, exist_ok=True)
        self.db_path = os.path.join(self.db_folder, db_name)
        self.conn = None

    def connect(self):
        """Conecta ao banco de dados."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
        return self.conn

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def _execute_script(self, script):
        """Executa um script SQL."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executescript(script)
        conn.commit()
        self.close() # Fecha a conexão após a operação

    def create_tables(self):
        """Cria as tabelas necessárias no banco de dados."""
        # Tabela Personagem
        personagem_table_sql = """
        CREATE TABLE IF NOT EXISTS personagens (
            nome TEXT PRIMARY KEY,
            jogador TEXT NOT NULL,
            raca_nome TEXT NOT NULL,
            classe_nome TEXT NOT NULL,
            nivel INTEGER NOT NULL,
            forca INTEGER NOT NULL,
            destreza INTEGER NOT NULL,
            constituicao INTEGER NOT NULL,
            inteligencia INTEGER NOT NULL,
            sabedoria INTEGER NOT NULL,
            carisma INTEGER NOT NULL,
            pontos_de_vida_max INTEGER,
            pontos_de_vida_atual INTEGER,
            pontos_de_experiencia INTEGER
        );
        """

        # Tabela para inventário (muitos para muitos) - Simplificado por enquanto
        # Itens seriam salvos separadamente e relacionados aqui.
        # Por enquanto, podemos salvar o inventário como JSON no personagem se for simples,
        # ou criar uma tabela 'itens' e 'personagem_inventario' para algo mais robusto.
        # Por simplicidade inicial, vamos considerar que o inventário pode ser salvo como JSON no Personagem.
        # Se os itens tiverem propriedades complexas, precisaremos de uma tabela 'itens' e um repositório para eles.

        # Tabela para armazenar atributos (opcional, se quiser flexibilidade para adicionar novos atributos)
        # Por enquanto, vou manter os atributos fixos na tabela de personagens,
        # mas essa é uma opção se você precisar de um esquema mais flexível.

        self._execute_script(personagem_table_sql)
        print("Tabelas verificadas/criadas com sucesso.")

# Para inicializar o banco de dados
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.create_tables()
    print(f"Banco de dados criado/verificado em: {db_manager.db_path}")