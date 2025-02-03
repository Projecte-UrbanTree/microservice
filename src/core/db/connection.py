from sqlmodel import Session, SQLModel, create_engine, select
from src.core.config import Settings
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(str(Settings.SQLALCHEMY_DATABASE_URI))

def get_session():
    with Session(engine) as session:
        yield session


