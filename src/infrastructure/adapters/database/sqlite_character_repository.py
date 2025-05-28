# src/infrastructure/adapters/database/sqlite_character_repository.py
import json
from typing import Optional, List

from src.infrastructure.repositories.personagem_repository import IPersonagemRepository
from src.domain.models.personagem import Personagem
from src.infrastructure.repositories.raca_repository import IRacaRepository # Precisamos para reconstruir o objeto Personagem
from src.infrastructure.repositories.classe_repository import IClasseRepository # Precisamos para reconstruir o objeto Personagem
from src.persistence.database_manager import DatabaseManager


class SQLitePersonagemRepository(IPersonagemRepository):
    def __init__(
        self,
        db_manager: DatabaseManager,
        raca_repository: IRacaRepository, # Recebe o repositório de raças
        classe_repository: IClasseRepository # Recebe o repositório de classes
    ):
        self._db_manager = db_manager
        self._raca_repository = raca_repository
        self._classe_repository = classe_repository

    def save(self, personagem: Personagem) -> None:
        conn = self._db_manager.connect()
        cursor = conn.cursor()

        # Armazenar inventário como JSON string para simplificar
        inventario_json = json.dumps([item.nome for item in personagem.inventario])

        cursor.execute("""
            INSERT OR REPLACE INTO personagens (
                nome, jogador, raca_nome, classe_nome, nivel,
                forca, destreza, constituicao, inteligencia, sabedoria, carisma,
                pontos_de_vida_max, pontos_de_vida_atual, pontos_de_experiencia
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            personagem.nome,
            personagem.jogador,
            personagem.raca.get("nome", personagem.raca_nome), # Usar o nome da raça
            personagem.classe.get("nome", personagem.classe_nome), # Usar o nome da classe
            personagem.nivel,
            personagem.atributos["forca"],
            personagem.atributos["destreza"],
            personagem.atributos["constituicao"],
            personagem.atributos["inteligencia"],
            personagem.atributos["sabedoria"],
            personagem.atributos["carisma"],
            personagem.pontos_de_vida_max,
            personagem.pontos_de_vida_atual,
            personagem.pontos_de_experiencia
            # inventario_json  # Se você adicionar a coluna de inventário
        ))
        conn.commit()
        self._db_manager.close()

    def get_by_name(self, nome: str) -> Optional[Personagem]:
        conn = self._db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personagens WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        self._db_manager.close()

        if row:
            # Reconstroi o objeto Personagem
            # Para isso, precisamos re-injettar os repositórios de raça e classe
            # ao criar a instância de Personagem a partir dos dados do DB.
            personagem = Personagem(
                nome=row['nome'],
                jogador=row['jogador'],
                raca_nome=row['raca_nome'],
                classe_nome=row['classe_nome'],
                nivel=row['nivel'],
                forca=row['forca'],
                destreza=row['destreza'],
                constituicao=row['constituicao'],
                inteligencia=row['inteligencia'],
                sabedoria=row['sabedoria'],
                carisma=row['carisma'],
                raca_repository=self._raca_repository,
                classe_repository=self._classe_repository
            )
            # Reaplicar pontos de vida, xp etc., que são gerenciados dinamicamente
            personagem.pontos_de_vida_max = row['pontos_de_vida_max']
            personagem.pontos_de_vida_atual = row['pontos_de_vida_atual']
            personagem.pontos_de_experiencia = row['pontos_de_experiencia']
            
            # Se você tivesse salvo o inventário como JSON
            # if 'inventario_json' in row and row['inventario_json']:
            #     inventario_nomes = json.loads(row['inventario_json'])
            #     # Aqui você precisaria de um ItemRepository para carregar os objetos Item
            #     # por enquanto, apenas salvamos os nomes
            #     personagem.inventario = [nome for nome in inventario_nomes]

            return personagem
        return None

    def get_all(self) -> List[Personagem]:
        conn = self._db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personagens")
        rows = cursor.fetchall()
        self._db_manager.close()

        personagens = []
        for row in rows:
            personagem = Personagem(
                nome=row['nome'],
                jogador=row['jogador'],
                raca_nome=row['raca_nome'],
                classe_nome=row['classe_nome'],
                nivel=row['nivel'],
                forca=row['forca'],
                destreza=row['destreza'],
                constituicao=row['constituicao'],
                inteligencia=row['inteligencia'],
                sabedoria=row['sabedoria'],
                carisma=row['carisma'],
                raca_repository=self._raca_repository,
                classe_repository=self._classe_repository
            )
            personagem.pontos_de_vida_max = row['pontos_de_vida_max']
            personagem.pontos_de_vida_atual = row['pontos_de_vida_atual']
            personagem.pontos_de_experiencia = row['pontos_de_experiencia']
            personagens.append(personagem)
        return personagens

    def delete(self, nome: str) -> None:
        conn = self._db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM personagens WHERE nome = ?", (nome,))
        conn.commit()
        self._db_manager.close()