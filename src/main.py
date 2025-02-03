from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints import sensors, test_db


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(sensors.router)
    app.include_router(test_db.router)
    return app


app: FastAPI = create_app()


@app.get("/health")
async def health():
    return {"status": "healthy"}
