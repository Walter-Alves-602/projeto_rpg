from enum import Enum
from pydantic import BaseModel, Field
import uuid

class PapelUsuario(str, Enum):
    JOGADOR = "jogador"
    MESTRE = "mestre"

class Usuario(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    hashed_password: str
    papel: PapelUsuario
