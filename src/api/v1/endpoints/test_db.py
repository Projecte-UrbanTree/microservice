from fastapi import APIRouter
from sqlalchemy import text
from src.core.db.connection import engine

router = APIRouter()


@router.get("/test_db", summary="Prueba directa de conexión a la base de datos")
async def test_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "success", "message": "Conexión a la base de datos exitosa"}
    except Exception as e:
        return {"status": "error", "message": f"Error al conectar con la base de datos: {str(e)}"}



