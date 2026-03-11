import sys
import os
from passlib.hash import bcrypt
from fastapi.templating import Jinja2Templates
from src.domain.services import AutenticacaoService
from src.infrastructure.adapters.database import SQLitePersonagemRepository, SQLiteMesaRepository, SQLiteUsuarioRepository
from src.infrastructure.adapters.data_files import ClasseFileAdapter, HabilidadesRaciaisFileAdapter, RacaFileAdapter
from src.persistence import DatabaseManager
from src.application.use_cases import GerenciarMesaUseCase, GerenciarPersonagemUseCase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

db_manager = DatabaseManager()
usuario_repository = SQLiteUsuarioRepository(db_manager)
autenticacao_service = AutenticacaoService(usuario_repository)
mesa_repository = SQLiteMesaRepository(db_manager)
personagem_repository = SQLitePersonagemRepository(db_manager)
raca_repository = RacaFileAdapter()
classe_repository = ClasseFileAdapter()
habilidades_raciais_repository = HabilidadesRaciaisFileAdapter()
gerenciar_mesa_uc = GerenciarMesaUseCase(mesa_repository, usuario_repository, personagem_repository)
gerenciar_personagem_uc = GerenciarPersonagemUseCase(personagem_repository, raca_repository, classe_repository, habilidades_raciais_repository)
templates = Jinja2Templates(directory="webapi/templates")
