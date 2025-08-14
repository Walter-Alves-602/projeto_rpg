from fastapi import APIRouter, Request, Form, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from webapi.dependencies import mesa_repository, usuario_repository, personagem_repository, gerenciar_mesa_uc, gerenciar_personagem_uc, templates

router = APIRouter()

@router.get("/mesa/{mesa_id}", response_class=HTMLResponse)
def mesa_page(request: Request, mesa_id: str):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = usuario_repository.buscar_por_id(usuario_id)
    mesa = mesa_repository.buscar_por_id(mesa_id)
    if not mesa:
        return HTMLResponse("<h2>Mesa não encontrada</h2>")
    mestres = [usuario_repository.buscar_por_id(uid).username for uid in getattr(mesa, 'mestres', []) if usuario_repository.buscar_por_id(uid)]
    jogadores = [usuario_repository.buscar_por_id(uid).username for uid in getattr(mesa, 'jogadores', []) if usuario_repository.buscar_por_id(uid)]
    personagens = [personagem_repository.buscar_por_id(pid) for pid in getattr(mesa, 'personagens', [])]
    personagens = [p for p in personagens if p]
    personagens_usuario = gerenciar_personagem_uc.listar_personagens_por_jogador(usuario_id)
    personagens_disponiveis = [p for p in personagens_usuario if p.id not in getattr(mesa, 'personagens', [])]
    todos_usuarios = [usuario_repository.buscar_por_id(uid) for uid in (getattr(mesa, 'mestres', []) + getattr(mesa, 'jogadores', [])) if usuario_repository.buscar_por_id(uid)]
    papel_usuario = usuario.papel.value if usuario else ""
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

@router.post("/mesa/{mesa_id}/adicionar_personagem")
def adicionar_personagem_mesa(request: Request, mesa_id: str, personagem_id: str = Form(...)):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    try:
        gerenciar_mesa_uc.adicionar_personagem_a_mesa(mesa_id, personagem_id, usuario_id)
    except Exception as e:
        return HTMLResponse(f"<h2>Erro ao adicionar personagem: {str(e)}</h2>")
    return RedirectResponse(url=f"/mesa/{mesa_id}", status_code=302)

@router.post("/mesa/{mesa_id}/adicionar_usuario", response_class=HTMLResponse)
def adicionar_usuario_mesa(request: Request, mesa_id: str, username: str = Form(...)):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    usuario = usuario_repository.buscar_por_id(usuario_id)
    if not usuario:
        return RedirectResponse(url="/login", status_code=302)
    usuario_adicionar = usuario_repository.buscar_por_username(username)
    if not usuario_adicionar:
        mesa = mesa_repository.buscar_por_id(mesa_id)
        mestres, jogadores, personagens, personagens_disponiveis, todos_usuarios, papel_usuario = [], [], [], [], [], ""
        if mesa:
            mestres = [usuario_repository.buscar_por_id(uid).username for uid in getattr(mesa, 'mestres', []) if usuario_repository.buscar_por_id(uid)]
            jogadores = [usuario_repository.buscar_por_id(uid).username for uid in getattr(mesa, 'jogadores', []) if usuario_repository.buscar_por_id(uid)]
            personagens = [personagem_repository.buscar_por_id(pid) for pid in getattr(mesa, 'personagens', [])]
            personagens = [p for p in personagens if p]
            personagens_usuario = gerenciar_personagem_uc.listar_personagens_por_jogador(usuario_id)
            personagens_disponiveis = [p for p in personagens_usuario if p.id not in getattr(mesa, 'personagens', [])]
            todos_usuarios = [usuario_repository.buscar_por_id(uid) for uid in (getattr(mesa, 'mestres', []) + getattr(mesa, 'jogadores', [])) if usuario_repository.buscar_por_id(uid)]
            papel_usuario = usuario.papel.value if usuario else ""
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
    try:
        gerenciar_mesa_uc.adicionar_usuario(mesa_id, username, usuario_id, usuario_adicionar.papel)
    except Exception as e:
        return HTMLResponse(f"<h2>Erro ao adicionar usuário: {str(e)}</h2>")
    return RedirectResponse(url=f"/mesa/{mesa_id}", status_code=302)

@router.get("/mesa/{mesa_id}/remover_usuario/{usuario_remover_id}")
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
    if usuario_remover_id in mesa.mestres:
        mesa.mestres.remove(usuario_remover_id)
    if usuario_remover_id in mesa.jogadores:
        mesa.jogadores.remove(usuario_remover_id)
    mesa_repository.salvar(mesa)
    return RedirectResponse(url=f"/mesa/{mesa_id}", status_code=302)

@router.get("/mesa/{mesa_id}/remover_personagem/{personagem_id}")
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
    if usuario.papel.value != "mestre" and personagem.jogador != usuario_id:
        return HTMLResponse("<h2>Permissão negada</h2>")
    if personagem_id in mesa.personagens:
        mesa.personagens.remove(personagem_id)
        mesa_repository.salvar(mesa)
    return RedirectResponse(url=f"/mesa/{mesa_id}", status_code=302)
