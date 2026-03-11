from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from webapi.dependencies import raca_repository, classe_repository, gerenciar_personagem_uc, templates

router = APIRouter()

@router.get("/criar_personagem", response_class=HTMLResponse)
def criar_personagem_form(request: Request):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    racas = raca_repository.get_all_raca_names() if hasattr(raca_repository, 'get_all_raca_names') else []
    classes = classe_repository.get_all_classe_names() if hasattr(classe_repository, 'get_all_classe_names') else []
    return templates.TemplateResponse("criar_personagem.html", {"request": request, "racas": racas, "classes": classes})

@router.post("/criar_personagem", response_class=HTMLResponse)
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
    raca = raca_repository.get_raca(raca_nome)
    if not raca:
        erro = f"Raça '{raca_nome}' não encontrada."
        racas = raca_repository.get_all_raca_names() if hasattr(raca_repository, 'get_all_raca_names') else []
        classes = classe_repository.get_all_classe_names() if hasattr(classe_repository, 'get_all_classe_names') else []
        return templates.TemplateResponse("criar_personagem.html", {"request": request, "erro": erro, "racas": racas, "classes": classes})
    mod_atributos = raca.get("atributos", {})
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
        racas = raca_repository.get_all_raca_names() if hasattr(raca_repository, 'get_all_raca_names') else []
        classes = classe_repository.get_all_classe_names() if hasattr(classe_repository, 'get_all_classe_names') else []
        return templates.TemplateResponse("criar_personagem.html", {"request": request, "erro": erro, "racas": racas, "classes": classes})
    return RedirectResponse(url="/user_page", status_code=302)
