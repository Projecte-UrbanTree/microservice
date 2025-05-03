from dotenv import load_dotenv
from sqlmodel import Session, create_engine

from src.core.config import settings

load_dotenv()
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_session():
    with Session(engine) as session:
        yield session
