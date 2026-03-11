from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from webapi.routes import auth_router, user_router, mesa_router , personagem_router, criar_personagem_router

app = FastAPI()
app.mount("/static"
, StaticFiles(directory="webapi/static"), name="static")
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(mesa_router)
app.include_router(personagem_router)
app.include_router(criar_personagem_router)
