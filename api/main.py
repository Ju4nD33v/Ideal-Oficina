from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.routes import clientes, dashboard, mecanicos, ordens, pecas, veiculos

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"

app = FastAPI(
    title="Ideal Oficina API",
    description="Sistema de gestão para oficinas mecânicas.",
    version="2.0.0",
)

app.include_router(dashboard.router)
app.include_router(clientes.router)
app.include_router(clientes.legacy_router)
app.include_router(veiculos.router)
app.include_router(mecanicos.router)
app.include_router(pecas.router)
app.include_router(ordens.router)

app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.get("/api/health", tags=["Sistema"])
def health():
    return {"status": "online", "application": "Ideal Oficina"}


@app.get("/", include_in_schema=False)
def interface():
    return FileResponse(WEB_DIR / "index.html")
