from fastapi import APIRouter
# Importa el engine definido en connection.py
from src.core.db.connection import engine

router = APIRouter()


@router.get("/test_db", summary="Prueba directa de conexión a la base de datos")
async def test_db_connection():
    try:
        # Abrir una conexión directamente a través del engine
        with engine.connect() as connection:
            # Ejecuta una consulta simple para verificar la conexión
            connection.execute("SELECT 1")
        return {"status": "success", "message": "Conexión a la base de datos exitosa"}
    except Exception as e:
        return {"status": "error", "message": f"Error al conectar con la base de datos: {str(e)}"}
