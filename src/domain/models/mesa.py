import uuid
from typing import List
from pydantic import BaseModel, Field

class Mesa(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nome: str
    descricao: str
    mestres: List[str] = Field(default_factory=list)  # Lista de IDs de usuários (mestres)
    jogadores: List[str] = Field(default_factory=list)  # Lista de IDs de usuários (jogadores)
    personagens: List[str] = Field(default_factory=list) # Lista de IDs de personagens
