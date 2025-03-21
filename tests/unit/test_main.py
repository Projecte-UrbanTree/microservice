from fastapi.testclient import TestClient
import os
from src.main import app

client = TestClient(app)

MAX_FILE_SIZE = 1024 * 1024
UPLOAD_DIR = "saved_files"
VALID_BODY = b"Hello, this is a test file."


def cleanup_saved_files():
    if os.path.exists(UPLOAD_DIR):
        for f in os.listdir(UPLOAD_DIR):
            os.remove(os.path.join(UPLOAD_DIR, f))


def test_upload_valid_file():
    cleanup_saved_files()
    response = client.post("/uploadFile?event=up", data=VALID_BODY)
    assert response.status_code == 200

    assert os.path.exists(UPLOAD_DIR), "El directorio de subida no existe."
    saved_files = os.listdir(UPLOAD_DIR)
    assert any(f.endswith(".json")
               for f in saved_files), "No se guardó ningún archivo con extensión .json."

    cleanup_saved_files()


def test_upload_large_file():
    cleanup_saved_files()
    large_content = b"A" * (MAX_FILE_SIZE + 1)
    response = client.post("/uploadFile?event=up", data=large_content)
    assert response.status_code == 403
    assert response.json()["detail"] == "File too large"


def test_upload_invalid_event():
    cleanup_saved_files()
    response = client.post("/uploadFile?event=invalid", data=VALID_BODY)
    assert response.status_code == 400
    assert "no implementado" in response.json()["detail"]


def test_upload_file_saves_correctly():
    cleanup_saved_files()
    file_content = b"Test file content"
    response = client.post("/uploadFile?event=up", data=file_content)
    assert response.status_code == 200

    saved_files = os.listdir(UPLOAD_DIR)
    matching_files = [f for f in saved_files if f.endswith(".json")]
    assert matching_files, "No se guardó ningún archivo con extensión .json."

    file_path = os.path.join(UPLOAD_DIR, matching_files[0])
    with open(file_path, "rb") as f:
        saved_content = f.read()
    assert saved_content == file_content

    cleanup_saved_files()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_sensors():
    response = client.get("/sensors?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list), "La respuesta no es una lista."


def test_get_sensor_by_id():
    response = client.get("/sensors/1")
    assert response.status_code == 200
    sensor = response.json()
    assert "id" in sensor, "El sensor no tiene un campo 'id'."
    assert sensor["id"] == 1, "El ID del sensor no coincide."
