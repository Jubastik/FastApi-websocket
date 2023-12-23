from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pages.router import router as router_pages
from chat.router import router as router_chat
import db_session

db_session.global_init()
app = FastAPI(
    title="Мой веб-сокет"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router_pages)
app.include_router(router_chat)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
