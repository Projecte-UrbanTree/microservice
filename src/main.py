from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from injector import Injector
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from sqlmodel import Session
from src.core.db.connection import get_session
from src.service.metrics_updater import update_all_metrics
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

    Instrumentator().instrument(app)

    injector = Injector([AppModule()])
    app.state.injector = injector

    app.include_router(sensors.router)
    return app


app: FastAPI = create_app()


@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/metrics", include_in_schema=False)
def metrics(session: Session = Depends(get_session)):
    update_all_metrics(session)
    data = generate_latest(REGISTRY)
    return Response(data, media_type=CONTENT_TYPE_LATEST)