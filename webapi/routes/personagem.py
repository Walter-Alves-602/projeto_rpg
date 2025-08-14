from fastapi import APIRouter, Request, Path
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import Query
from webapi.dependencies import personagem_repository, habilidades_raciais_repository, templates

router = APIRouter()

@router.get("/personagem/{personagem_id}", response_class=HTMLResponse)
def exibir_personagem(request: Request, personagem_id: str = Path(...)):
    usuario_id = request.cookies.get("user_id")
    if not usuario_id:
        return RedirectResponse(url="/login", status_code=302)
    personagem = personagem_repository.buscar_por_id(personagem_id)
    if not personagem:
        return HTMLResponse("<h2>Personagem não encontrado</h2>")
    habilidades = []
    for h_nome in getattr(personagem, "habilidades_raciais", []):
        desc = habilidades_raciais_repository.get_habilidade_descricao(h_nome)
        habilidades.append({"nome": h_nome, "descricao": desc})
    for h in getattr(personagem, "habilidades_extras", []):
        if isinstance(h, dict):
            habilidades.append({"nome": h.get("nome", ""), "descricao": h.get("descricao", "")})
        else:
            habilidades.append({"nome": str(h), "descricao": ""})
    ficha = {
        "nome": personagem.nome,
        "classe_nome": getattr(personagem, "classe_nome", ""),
        "nivel": getattr(personagem, "nivel", 1),
        "raca_nome": getattr(personagem, "raca_nome", ""),
        "bonus_proficiencia": getattr(personagem, "bonus_proficiencia", 2),
        "forca": getattr(personagem, "forca", 10),
        "destreza": getattr(personagem, "destreza", 10),
        "constituicao": getattr(personagem, "constituicao", 10),
        "inteligencia": getattr(personagem, "inteligencia", 10),
        "sabedoria": getattr(personagem, "sabedoria", 10),
        "carisma": getattr(personagem, "carisma", 10),
        "pericias": getattr(personagem, "pericias", []),
        "pv_atual": getattr(personagem, "pv_atual", 0),
        "pv_max": getattr(personagem, "pv_max", 0),
        "ca": getattr(personagem, "ca", 10),
        "iniciativa": getattr(personagem, "iniciativa", 0),
        "magias": getattr(personagem, "magias", []),
        "inventario": getattr(personagem, "inventario", []),
        "anotacoes": getattr(personagem, "anotacoes", ""),
        "xp": getattr(personagem, "xp", 0),
        "proxima_sessao": getattr(personagem, "proxima_sessao", ""),
        "habilidades": habilidades,
        "id": personagem.id,
    }
    return templates.TemplateResponse("personagem_page.html", {"request": request, "personagem": ficha})

@router.get("/rolar_dado")
def rolar_dado_endpoint(lados: int = Query(...)):
    import random
    resultado = random.randint(1, lados)
    return JSONResponse(content={"resultado": resultado})
