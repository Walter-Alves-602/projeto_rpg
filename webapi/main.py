from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.domain.services import AutenticacaoService
from src.infrastructure.adapters.database import SQLiteUsuarioRepository
from src.persistence import DatabaseManager
from src.infrastructure.adapters.data_files import (
    ClasseFileAdapter,
    HabilidadesRaciaisFileAdapter,
    RacaFileAdapter,
)
from src.infrastructure.adapters.database import (
    SQLitePersonagemRepository,
    SQLiteMesaRepository,
)
from src.application.use_cases import GerenciarMesaUseCase, GerenciarPersonagemUseCase


# Dependências para os casos de uso e app
db_manager = DatabaseManager()
usuario_repository = SQLiteUsuarioRepository(db_manager)
autenticacao_service = AutenticacaoService(usuario_repository)
mesa_repository = SQLiteMesaRepository(db_manager)
personagem_repository = SQLitePersonagemRepository(db_manager)
raca_repository = RacaFileAdapter()
classe_repository = ClasseFileAdapter()
habilidades_raciais_repository = HabilidadesRaciaisFileAdapter()
gerenciar_mesa_uc = GerenciarMesaUseCase(
    mesa_repository, usuario_repository, personagem_repository
)
gerenciar_personagem_uc = GerenciarPersonagemUseCase(
    personagem_repository, raca_repository, classe_repository, habilidades_raciais_repository
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="webapi/static"), name="static")
templates = Jinja2Templates(directory="webapi/templates")


# --- Login com autenticação real e cookie de sessão ---
@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    user = autenticacao_service.autenticar_usuario(username, password)
    if user:
        response = RedirectResponse(url="/user_page", status_code=302)
        response.set_cookie(key="user_id", value=user.id, httponly=True, max_age=60*60*24)
        return response
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Usuário ou senha inválidos."})


# --- Página do Usuário autenticada ---
@app.get("/user_page", response_class=HTMLResponse)
def user_page(request: Request):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = usuario_repository.buscar_por_id(usuario_id)
    if not usuario:
        response = RedirectResponse(url="/login", status_code=302)
        response.delete_cookie("user_id")
        return response
    username = usuario.username
    papel = usuario.papel.value
    mesas = [
        {"id": m.id, "nome": m.nome, "criador": usuario_repository.buscar_por_id(m.mestres[0]).username if m.mestres else "-"}
        for m in gerenciar_mesa_uc.listar_mesas_do_usuario(usuario_id)
    ]
    personagens = [
        {"nome": p.nome, "nivel": p.nivel, "raca": p.raca_nome, "classe": p.classe_nome}
        for p in gerenciar_personagem_uc.listar_personagens_por_jogador(usuario_id)
    ]
    return templates.TemplateResponse(
        "user_page.html",
        {"request": request, "username": username, "papel": papel, "mesas": mesas, "personagens": personagens}
    )

# --- Logout ---
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("user_id")
    return response
    
# --- Criar Mesa (POST do modal) ---
@app.post("/create_mesa")
def create_mesa(request: Request, nome: str = Form(...), descricao: str = Form(...)):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = usuario_repository.buscar_por_id(usuario_id)
    if not usuario or usuario.papel.value != "mestre":
        return HTMLResponse("<h2>Permissão negada</h2>")
    try:
        gerenciar_mesa_uc.criar_mesa(nome=nome, descricao=descricao, mestre_id=usuario_id)
    except Exception as e:
        return HTMLResponse(f"<h2>Erro ao criar mesa: {str(e)}</h2>")
    return RedirectResponse(url="/user_page", status_code=302)
