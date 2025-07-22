import json
from typing import Optional, List
from src.infrastructure.repositories import IPersonagemRepository,IRacaRepository,IClasseRepository,IHabilidadesRaciaisRepository
from src.domain.models import Personagem
from src.persistence import DatabaseManager


class SQLitePersonagemRepository(IPersonagemRepository):
    def __init__(
        self,
        db_manager: DatabaseManager,
        raca_repository: IRacaRepository,
        classe_repository: IClasseRepository,
        habilidades_raciais_repository: IHabilidadesRaciaisRepository,
    ):
        self._db_manager = db_manager
        self._raca_repository = raca_repository
        self._classe_repository = classe_repository
        self._habilidades_raciais_repository = habilidades_raciais_repository

    def save(self, personagem: Personagem) -> None:
        conn = self._db_manager.connect()
        cursor = conn.cursor()

        # Serializa a lista de habilidades raciais para uma string JSON
        habilidades_raciais_json = json.dumps(personagem.habilidades_raciais_nomes)

        cursor.execute(
            """
            INSERT OR REPLACE INTO personagens (
                nome, jogador, raca_nome, classe_nome, nivel,
                forca, destreza, constituicao, inteligencia, sabedoria, carisma,
                pontos_de_vida_max, pontos_de_vida_atual, pontos_de_experiencia,
                deslocamento,
                habilidades_raciais -- <-- NOVIDADE AQUI: Adiciona a coluna no INSERT
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                personagem.nome,
                personagem.jogador,
                personagem.raca_nome,
                personagem.classe_nome,
                personagem.nivel,
                personagem.atributos["forca"],
                personagem.atributos["destreza"],
                personagem.atributos["constituicao"],
                personagem.atributos["inteligencia"],
                personagem.atributos["sabedoria"],
                personagem.atributos["carisma"],
                personagem.pontos_de_vida_max,
                personagem.pontos_de_vida_atual,
                personagem.pontos_de_experiencia,
                personagem.deslocamento,
                habilidades_raciais_json,  # <-- NOVIDADE AQUI: Passa a string JSON
            ),
        )
        conn.commit()
        self._db_manager.close(conn)

    def get_by_name(self, nome: str) -> Optional[Personagem]:
        conn = self._db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personagens WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        self._db_manager.close(conn)

        if row:
            # Desserializa a string JSON de habilidades raciais de volta para uma lista Python
            habilidades_raciais_nomes = (
                json.loads(row["habilidades_raciais"])
                if row["habilidades_raciais"]
                else []
            )

            personagem = Personagem(
                nome=row["nome"],
                jogador=row["jogador"],
                raca_nome=row["raca_nome"],
                classe_nome=row["classe_nome"],
                nivel=row["nivel"],
                forca=row["forca"],
                destreza=row["destreza"],
                constituicao=row["constituicao"],
                inteligencia=row["inteligencia"],
                sabedoria=row["sabedoria"],
                carisma=row["carisma"],
                raca_repository=self._raca_repository,
                classe_repository=self._classe_repository,
            )
            personagem.pontos_de_vida_max = row["pontos_de_vida_max"]
            personagem.pontos_de_vida_atual = row["pontos_de_vida_atual"]
            personagem.pontos_de_experiencia = row["pontos_de_experiencia"]
            personagem.deslocamento = row["deslocamento"]
            personagem.habilidades_raciais_nomes = habilidades_raciais_nomes

            return personagem
        return None

    def get_all(self) -> List[Personagem]:
        conn = self._db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personagens")
        rows = cursor.fetchall()
        self._db_manager.close(conn)

        personagens = []
        for row in rows:
            # Desserializa a string JSON de habilidades raciais de volta para uma lista Python
            habilidades_raciais_nomes = (
                json.loads(row["habilidades_raciais"])
                if row["habilidades_raciais"]
                else []
            )

            personagem = Personagem(
                nome=row["nome"],
                jogador=row["jogador"],
                raca_nome=row["raca_nome"],
                classe_nome=row["classe_nome"],
                nivel=row["nivel"],
                forca=row["forca"],
                destreza=row["destreza"],
                constituicao=row["constituicao"],
                inteligencia=row["inteligencia"],
                sabedoria=row["sabedoria"],
                carisma=row["carisma"],
                raca_repository=self._raca_repository,
                classe_repository=self._classe_repository,
            )
            personagem.pontos_de_vida_max = row["pontos_de_vida_max"]
            personagem.pontos_de_vida_atual = row["pontos_de_vida_atual"]
            personagem.pontos_de_experiencia = row["pontos_de_experiencia"]
            personagem.deslocamento = row["deslocamento"]
            personagem.habilidades_raciais_nomes = habilidades_raciais_nomes
            personagens.append(personagem)
        return personagens

    def delete(self, nome: str) -> None:
        conn = self._db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personagens WHERE nome = ?", (nome,))
        conn.commit()
        self._db_manager.close(conn)
