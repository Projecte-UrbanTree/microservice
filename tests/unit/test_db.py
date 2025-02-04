# tests/unit/test_db.py
import pytest
from sqlalchemy import text
from src.core.db.connection import engine


def test_engine_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            row = result.fetchone()
            assert row is not None, "No se obtuvo ningún resultado"
            assert row[0] == 1, "El resultado de la consulta no es 1"
    except Exception as e:
        pytest.fail(f"No se pudo conectar a la base de datos: {str(e)}")
