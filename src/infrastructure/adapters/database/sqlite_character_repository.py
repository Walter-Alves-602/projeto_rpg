import json
from typing import List, Optional

from src.domain.models import Personagem
from src.domain.ports import PersonagemRepositoryPort
from src.persistence import DatabaseManager


class SQLitePersonagemRepository(PersonagemRepositoryPort):
    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager

    def _row_to_personagem(self, row) -> Personagem:
        """Converte uma linha do banco de dados em um objeto Personagem."""
        return Personagem(
            id=row["id"],
            nome=row["nome"],
            jogador=row["jogador"],
            raca_nome=row["raca_nome"],
            classe_nome=row["classe_nome"],
            nivel=row["nivel"],
            pontos_de_experiencia=row["pontos_de_experiencia"],
            forca=row["forca"],
            destreza=row["destreza"],
            constituicao=row["constituicao"],
            inteligencia=row["inteligencia"],
            sabedoria=row["sabedoria"],
            carisma=row["carisma"],
            pontos_de_vida_max=row["pontos_de_vida_max"],
            pontos_de_vida_atual=row["pontos_de_vida_atual"],
            deslocamento=row["deslocamento"],
            habilidades_raciais=json.loads(row["habilidades_raciais"] or '[]'),
            habilidades_extras=json.loads(row["habilidades_extras"] or '[]'),
            proficiencias_armas=json.loads(row["proficiencias_armas"] or '[]'),
            proficiencias_armaduras=json.loads(row["proficiencias_armaduras"] or '[]'),
            testes_de_resistencia=json.loads(row["testes_de_resistencia"] or '[]'),
            pericias_escolhidas=json.loads(row["pericias_escolhidas"] or '[]'),
            inventario=json.loads(row["inventario"] or '[]'),
            linguas=json.loads(row["linguas"] or '[]'),
            ferramentas=json.loads(row["ferramentas"] or '[]'),
        )

    def salvar(self, personagem: Personagem) -> None:
        query = """
            INSERT OR REPLACE INTO personagens (
                id, nome, jogador, raca_nome, classe_nome, nivel, pontos_de_experiencia,
                forca, destreza, constituicao, inteligencia, sabedoria, carisma,
                pontos_de_vida_max, pontos_de_vida_atual, deslocamento, habilidades_raciais,
                habilidades_extras, proficiencias_armas, proficiencias_armaduras,
                testes_de_resistencia, pericias_escolhidas, inventario, linguas, ferramentas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            personagem.id, personagem.nome, personagem.jogador, personagem.raca_nome, 
            personagem.classe_nome, personagem.nivel, personagem.pontos_de_experiencia,
            personagem.forca, personagem.destreza, personagem.constituicao, 
            personagem.inteligencia, personagem.sabedoria, personagem.carisma,
            personagem.pontos_de_vida_max, personagem.pontos_de_vida_atual, personagem.deslocamento,
            json.dumps(personagem.habilidades_raciais), json.dumps(personagem.habilidades_extras),
            json.dumps(personagem.proficiencias_armas), json.dumps(personagem.proficiencias_armaduras),
            json.dumps(personagem.testes_de_resistencia), json.dumps(personagem.pericias_escolhidas),
            json.dumps(personagem.inventario), json.dumps(personagem.linguas), json.dumps(personagem.ferramentas)
        )
        self._db_manager.execute_query(query, params)

    def buscar_por_id(self, personagem_id: str) -> Optional[Personagem]:
        query = "SELECT * FROM personagens WHERE id = ?"
        row = self._db_manager.fetch_one(query, (personagem_id,))
        return self._row_to_personagem(row) if row else None

    def buscar_por_nome(self, nome: str) -> Optional[Personagem]:
        query = "SELECT * FROM personagens WHERE nome = ?"
        row = self._db_manager.fetch_one(query, (nome,))
        return self._row_to_personagem(row) if row else None

    def listar_todos(self) -> List[Personagem]:
        query = "SELECT * FROM personagens"
        rows = self._db_manager.fetch_all(query)
        return [self._row_to_personagem(row) for row in rows]

    def deletar(self, personagem_id: str) -> None:
        query = "DELETE FROM personagens WHERE id = ?"
        self._db_manager.execute_query(query, (personagem_id,))

    def listar_por_ids(self, personagem_ids: List[str]) -> List[Personagem]:
        if not personagem_ids:
            return []
        placeholders = ",".join("?" for _ in personagem_ids)
        query = f"SELECT * FROM personagens WHERE id IN ({placeholders})"
        rows = self._db_manager.fetch_all(query, personagem_ids)
        return [self._row_to_personagem(row) for row in rows]

    def listar_por_mesa(self, mesa_id):
        query = """SELECT p.* FROM personagens p
                   JOIN mesas_personagens mp ON p.id = mp.personagem_id
                   WHERE mp.mesa_id = ?"""
        rows = self._db_manager.fetch_all(query, (mesa_id,))
        return [self._row_to_personagem(row) for row in rows]
