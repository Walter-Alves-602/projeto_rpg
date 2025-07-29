# src/persistence/database_manager.py
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="rpg_characters.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)

    def connect(self):
        """Estabelece e retorna uma conexão com o banco de dados."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Isso permite acessar colunas por nome
        return conn

    def create_tables(self):
        """Cria as tabelas necessárias no banco de dados, se elas não existirem."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
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
                pontos_de_experiencia INTEGER,
                deslocamento REAL,
                habilidades_raciais TEXT,
                habilidades_extras TEXT
            )
        """)
        conn.commit()
        # Garante que a conexão seja fechada após a criação das tabelas
        self.close(conn) 

    # IMPORTANTE: ESTE MÉTODO PRECISA ESTAR AQUI DENTRO DA CLASSE DatabaseManager!
    def close(self, conn): 
        """Fecha a conexão com o banco de dados."""
        conn.close()