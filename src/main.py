from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from injector import Injector
from prometheus_fastapi_instrumentator import Instrumentator

from src.api.v1.endpoints import sensors
from src.core.di import AppModule


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Instrumentator().instrument(app).expose(app)

    injector = Injector([AppModule()])
    app.state.injector = injector

    app.include_router(sensors.router)
    return app


app: FastAPI = create_app()


@app.get("/health")
async def health():
    return {"status": "healthy"}
