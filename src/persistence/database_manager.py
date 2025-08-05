# src/persistence/database_manager.py
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="rpg_characters.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)

    def connect(self):
        """Estabelece e retorna uma conexão com o banco de dados."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self):
        """Cria ou atualiza as tabelas necessárias no banco de dados."""
        conn = self.connect()
        cursor = conn.cursor()

        # Tabela de Usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL,
                papel TEXT NOT NULL
            )
        """)

        # Tabela de Personagens
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personagens (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                jogador TEXT NOT NULL,
                raca_nome TEXT NOT NULL,
                classe_nome TEXT NOT NULL,
                nivel INTEGER NOT NULL,
                pontos_de_experiencia INTEGER NOT NULL,
                forca INTEGER NOT NULL,
                destreza INTEGER NOT NULL,
                constituicao INTEGER NOT NULL,
                inteligencia INTEGER NOT NULL,
                sabedoria INTEGER NOT NULL,
                carisma INTEGER NOT NULL,
                pontos_de_vida_max INTEGER NOT NULL,
                pontos_de_vida_atual INTEGER NOT NULL,
                deslocamento REAL NOT NULL,
                habilidades_raciais TEXT,
                habilidades_extras TEXT,
                proficiencias_armas TEXT,
                proficiencias_armaduras TEXT,
                testes_de_resistencia TEXT,
                pericias_escolhidas TEXT,
                inventario TEXT,
                linguas TEXT,
                ferramentas TEXT
            )
        """)

        # Tabela de Mesas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mesas (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                descricao TEXT
            )
        """)

        # Tabela de Associação Mesas-Usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mesas_usuarios (
                mesa_id TEXT NOT NULL,
                usuario_id TEXT NOT NULL,
                papel TEXT NOT NULL, -- 'mestre' ou 'jogador'
                PRIMARY KEY (mesa_id, usuario_id),
                FOREIGN KEY (mesa_id) REFERENCES mesas(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        # Tabela de Associação Mesas-Personagens
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mesas_personagens (
                mesa_id TEXT NOT NULL,
                personagem_id TEXT NOT NULL,
                PRIMARY KEY (mesa_id, personagem_id),
                FOREIGN KEY (mesa_id) REFERENCES mesas(id),
                FOREIGN KEY (personagem_id) REFERENCES personagens(id)
            )
        """)

        conn.commit()
        self.close(conn)

    def close(self, conn):
        """Fecha a conexão com o banco de dados."""
        conn.close()

    def fetch_one(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        row = cursor.fetchone()
        self.close(conn)
        return row

    def fetch_all(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        self.close(conn)
        return rows

    def execute_query(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        self.close(conn)