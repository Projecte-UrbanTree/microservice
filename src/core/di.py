# src/core/di.py
from injector import Module, provider, singleton
from sqlmodel import Session
from src.service.file_service import FileService
from src.core.db.connection import engine


class AppModule(Module):
    @singleton
    @provider
    def provide_session(self) -> Session:
        return Session(engine)

    @singleton
    @provider
    def provide_file_service(self, session: Session) -> FileService:
        return FileService(session)
