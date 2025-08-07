import sys
import os
from passlib.hash import bcrypt
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.domain.models import PapelUsuario, Usuario
from src.domain.services import AutenticacaoService
from src.infrastructure.adapters.database import (
    SQLitePersonagemRepository,
    SQLiteMesaRepository,
    SQLiteUsuarioRepository
)
from src.infrastructure.adapters.data_files import (
    ClasseFileAdapter,
    HabilidadesRaciaisFileAdapter,
    RacaFileAdapter,
)
from src.persistence import DatabaseManager
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

# --- Registrar Usuário ---
@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
def register_submit(request: Request, username: str = Form(...), password: str = Form(...), role: str = Form(...)):
    if usuario_repository.buscar_por_username(username):
        return templates.TemplateResponse("register.html", {"request": request, "error": "Usuário já existe."})
    try:
        papel = PapelUsuario[role.upper()]
    except Exception:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Papel inválido."})
    hashed_password = bcrypt.hash(password)
    novo_usuario = Usuario(username=username, hashed_password=hashed_password, papel=papel)
    usuario_repository.salvar(novo_usuario)
    # Login automático
    response = RedirectResponse(url="/user_page", status_code=302)
    response.set_cookie(key="user_id", value=novo_usuario.id, httponly=True, max_age=60*60*24)
    return response


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
        {
            "id": m.id,
            "nome": m.nome,
            "descricao": m.descricao,
            "criador": usuario_repository.buscar_por_id(m.mestres[0]).username if m.mestres else "-"
        }
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

# --- Página da Mesa ---
@app.get("/mesa/{mesa_id}", response_class=HTMLResponse)
def mesa_page(request: Request, mesa_id: str):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = usuario_repository.buscar_por_id(usuario_id)
    mesa = mesa_repository.buscar_por_id(mesa_id)
    if not mesa:
        return HTMLResponse("<h2>Mesa não encontrada</h2>")
    mestres = [usuario_repository.buscar_por_id(uid).username for uid in mesa.mestres]
    jogadores = [usuario_repository.buscar_por_id(uid).username for uid in mesa.jogadores]
    personagens = [personagem_repository.buscar_por_id(pid) for pid in mesa.personagens]
    personagens = [p for p in personagens if p]
    # Personagens disponíveis para adicionar (do usuário, que não estão na mesa)
    personagens_usuario = gerenciar_personagem_uc.listar_personagens_por_jogador(usuario_id)
    personagens_disponiveis = [p for p in personagens_usuario if p.id not in mesa.personagens]
    # Todos usuários da mesa (mestres + jogadores)
    todos_usuarios = [usuario_repository.buscar_por_id(uid) for uid in (mesa.mestres + mesa.jogadores)]
    papel_usuario = usuario.papel.value
    def pode_remover_personagem(p):
        if papel_usuario == 'mestre':
            return True
        return p.jogador == usuario_id
    return templates.TemplateResponse(
        "mesa_page.html",
        {
            "request": request,
            "mesa": mesa,
            "mestres": mestres,
            "jogadores": jogadores,
            "personagens": personagens,
            "personagens_disponiveis": personagens_disponiveis,
            "todos_usuarios": todos_usuarios,
            "usuario_id": usuario_id,
            "papel_usuario": papel_usuario,
            "pode_remover_personagem": pode_remover_personagem,
        }
    )

# --- Adicionar personagem à mesa ---
@app.post("/mesa/{mesa_id}/adicionar_personagem")
def adicionar_personagem_mesa(request: Request, mesa_id: str, personagem_id: str = Form(...)):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    try:
        gerenciar_mesa_uc.adicionar_personagem_a_mesa(mesa_id, personagem_id, usuario_id)
    except Exception as e:
        return HTMLResponse(f"<h2>Erro ao adicionar personagem: {str(e)}</h2>")
    return RedirectResponse(url=f"/mesa/{mesa_id}", status_code=302)

# --- Adicionar usuário à mesa pelo nome de usuário ---
@app.post("/mesa/{mesa_id}/adicionar_usuario", response_class=HTMLResponse)
def adicionar_usuario_mesa(request: Request, mesa_id: str, username: str = Form(...)):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = usuario_repository.buscar_por_id(usuario_id)
    if not usuario:
        return RedirectResponse(url="/login", status_code=302)
    usuario_adicionar = usuario_repository.buscar_por_username(username)
    if not usuario_adicionar:
        # Renderizar a página da mesa com mensagem de erro
        mesa = mesa_repository.buscar_por_id(mesa_id)
        mestres = [usuario_repository.buscar_por_id(uid).username for uid in mesa.mestres]
        jogadores = [usuario_repository.buscar_por_id(uid).username for uid in mesa.jogadores]
        personagens = [personagem_repository.buscar_por_id(pid) for pid in mesa.personagens]
        personagens = [p for p in personagens if p]
        personagens_usuario = gerenciar_personagem_uc.listar_personagens_por_jogador(usuario_id)
        personagens_disponiveis = [p for p in personagens_usuario if p.id not in mesa.personagens]
        todos_usuarios = [usuario_repository.buscar_por_id(uid) for uid in (mesa.mestres + mesa.jogadores)]
        papel_usuario = usuario.papel.value
        def pode_remover_personagem(p):
            if papel_usuario == 'mestre':
                return True
            return p.jogador == usuario_id
        return templates.TemplateResponse(
            "mesa_page.html",
            {
                "request": request,
                "mesa": mesa,
                "mestres": mestres,
                "jogadores": jogadores,
                "personagens": personagens,
                "personagens_disponiveis": personagens_disponiveis,
                "todos_usuarios": todos_usuarios,
                "usuario_id": usuario_id,
                "papel_usuario": papel_usuario,
                "pode_remover_personagem": pode_remover_personagem,
                "erro_adicionar_usuario": f"Usuário '{username}' não encontrado."
            }
        )
    # Adiciona o usuário à mesa de acordo com seu papel
    try:
        gerenciar_mesa_uc.adicionar_usuario(mesa_id, username, usuario_id, usuario_adicionar.papel)
    except Exception as e:
        return HTMLResponse(f"<h2>Erro ao adicionar usuário: {str(e)}</h2>")
    return RedirectResponse(url=f"/mesa/{mesa_id}", status_code=302)

    # --- Remover usuário da mesa ---
@app.get("/mesa/{mesa_id}/remover_usuario/{usuario_remover_id}")
def remover_usuario_mesa(request: Request, mesa_id: str, usuario_remover_id: str):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = usuario_repository.buscar_por_id(usuario_id)
    if not usuario or usuario.papel.value != "mestre":
        return HTMLResponse("<h2>Permissão negada</h2>")
    mesa = mesa_repository.buscar_por_id(mesa_id)
    if not mesa:
        return HTMLResponse("<h2>Mesa não encontrada</h2>")
    # Remover usuário da mesa (de mestres ou jogadores)
    if usuario_remover_id in mesa.mestres:
        mesa.mestres.remove(usuario_remover_id)
    if usuario_remover_id in mesa.jogadores:
        mesa.jogadores.remove(usuario_remover_id)
    mesa_repository.salvar(mesa)
    return RedirectResponse(url=f"/mesa/{mesa_id}", status_code=302)

# --- Remover personagem da mesa ---
@app.get("/mesa/{mesa_id}/remover_personagem/{personagem_id}")
def remover_personagem_mesa(request: Request, mesa_id: str, personagem_id: str):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = usuario_repository.buscar_por_id(usuario_id)
    mesa = mesa_repository.buscar_por_id(mesa_id)
    if not usuario or not mesa:
        return HTMLResponse("<h2>Permissão negada ou mesa não encontrada</h2>")
    personagem = personagem_repository.buscar_por_id(personagem_id)
    if not personagem:
        return HTMLResponse("<h2>Personagem não encontrado</h2>")
    # Permissão: mestre pode remover qualquer um, jogador só pode remover seus próprios
    if usuario.papel.value != "mestre" and personagem.jogador != usuario_id:
        return HTMLResponse("<h2>Permissão negada</h2>")
    if personagem_id in mesa.personagens:
        mesa.personagens.remove(personagem_id)
        mesa_repository.salvar(mesa)
    return RedirectResponse(url=f"/mesa/{mesa_id}", status_code=302)

# --- Página de criação de personagem ---
@app.get("/criar_personagem", response_class=HTMLResponse)
def criar_personagem_form(request: Request):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    racas = raca_repository.listar_racas() if hasattr(raca_repository, 'listar_racas') else []
    classes = classe_repository.listar_classes() if hasattr(classe_repository, 'listar_classes') else []
    return templates.TemplateResponse("criar_personagem.html", {"request": request, "racas": racas, "classes": classes})

@app.post("/criar_personagem", response_class=HTMLResponse)
def criar_personagem_submit(request: Request,
    nome: str = Form(...),
    raca_nome: str = Form(...),
    classe_nome: str = Form(...),
    nivel: int = Form(...),
    forca: int = Form(...),
    destreza: int = Form(...),
    constituicao: int = Form(...),
    inteligencia: int = Form(...),
    sabedoria: int = Form(...),
    carisma: int = Form(...)):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    # Busca modificadores da raça
    raca = raca_repository.get_raca(raca_nome)
    if not raca:
        erro = f"Raça '{raca_nome}' não encontrada."
        racas = raca_repository.listar_racas() if hasattr(raca_repository, 'listar_racas') else []
        classes = classe_repository.listar_classes() if hasattr(classe_repository, 'listar_classes') else []
        return templates.TemplateResponse("criar_personagem.html", {"request": request, "erro": erro, "racas": racas, "classes": classes})
    # Aplica modificadores da raça
    mod_atributos = raca.get("modificadores", {})
    dados = {
        "nome": nome,
        "jogador": usuario_id,
        "raca_nome": raca_nome,
        "classe_nome": classe_nome,
        "nivel": nivel,
        "forca": forca + mod_atributos.get("forca", 0),
        "destreza": destreza + mod_atributos.get("destreza", 0),
        "constituicao": constituicao + mod_atributos.get("constituicao", 0),
        "inteligencia": inteligencia + mod_atributos.get("inteligencia", 0),
        "sabedoria": sabedoria + mod_atributos.get("sabedoria", 0),
        "carisma": carisma + mod_atributos.get("carisma", 0),
    }
    try:
        gerenciar_personagem_uc.criar_personagem(dados)
    except Exception as e:
        erro = f"Erro ao criar personagem: {str(e)}"
        racas = raca_repository.listar_racas() if hasattr(raca_repository, 'listar_racas') else []
        classes = classe_repository.listar_classes() if hasattr(classe_repository, 'listar_classes') else []
        return templates.TemplateResponse("criar_personagem.html", {"request": request, "erro": erro, "racas": racas, "classes": classes})
    return RedirectResponse(url="/user_page", status_code=302)