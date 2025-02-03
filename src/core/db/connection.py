# src/core/db/connection.py
from sqlmodel import Session, create_engine
from src.core.config import settings
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_session():
    with Session(engine) as session:
        yield session
