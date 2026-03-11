from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from webapi.dependencies import usuario_repository, templates, gerenciar_mesa_uc, gerenciar_personagem_uc

router = APIRouter()

@router.get("/user_page", response_class=HTMLResponse)
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
            "criador": usuario_repository.buscar_por_id(m.mestres[0]).username if m.mestres and usuario_repository.buscar_por_id(m.mestres[0]) else "-" # type: ignore
        }
        for m in gerenciar_mesa_uc.listar_mesas_do_usuario(usuario_id)
    ]
    personagens = [
        {"id": p.id, "nome": p.nome, "nivel": p.nivel, "raca": p.raca_nome, "classe": p.classe_nome}
        for p in gerenciar_personagem_uc.listar_personagens_por_jogador(usuario_id)
    ]
    return templates.TemplateResponse(
        "user_page.html",
        {"request": request, "username": username, "papel": papel, "mesas": mesas, "personagens": personagens}
    )
