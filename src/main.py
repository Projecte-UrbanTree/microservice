from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.v1.pages import pages
from src.api.v1.endpoints import sensors


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount("/static", StaticFiles(directory="src/static"), name="static")
    app.include_router(sensors.router)
    app.include_router(pages.router)
    return app


app: FastAPI = create_app()

@app.get("/health")
async def health():
    return { "status": "healthy" }




