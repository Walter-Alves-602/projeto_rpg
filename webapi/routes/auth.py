from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from passlib.hash import bcrypt
from webapi.dependencies import usuario_repository, autenticacao_service, templates
from src.domain.models import PapelUsuario, Usuario

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    user = autenticacao_service.autenticar_usuario(username, password)
    if user:
        response = RedirectResponse(url="/user_page", status_code=302)
        response.set_cookie(key="user_id", value=user.id, httponly=True, max_age=60*60*24)
        return response
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Usuário ou senha inválidos."})

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
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
    response = RedirectResponse(url="/user_page", status_code=302)
    response.set_cookie(key="user_id", value=novo_usuario.id, httponly=True, max_age=60*60*24)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("user_id")
    return response
