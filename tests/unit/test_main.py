from fastapi.testclient import TestClient
import os
from src.main import app

client = TestClient(app)


MAX_FILE = 1024 * 1024
ALLOWED_EXTENSIONS = {".txt", ".jpg", ".png"}
UPLOAD_DIR = "uploads"

client = TestClient(app)


def test_upload_valid_file():
    file_content = b"Hello, this is a test file."
    files = {"uploadedFile": ("test.txt", file_content, "text/plain")}

    response = client.post("/uploadFile", files=files)

    assert response.status_code == 200
    data = response.json()

    assert data["filename"] == "test.txt"
    assert data["saved_as"].endswith(".txt")
    assert os.path.exists(os.path.join(data["file_location"], data["saved_as"]))


def test_upload_large_file():
    large_content = b"A" * (MAX_FILE + 1)
    files = {"uploadedFile": ("large.txt", large_content, "text/plain")}

    response = client.post("/uploadFile", files=files)

    assert response.status_code == 403
    assert response.json()["detail"] == "File too large"


def test_upload_invalid_extension():
    file_content = b"Invalid file format test"
    files = {"uploadedFile": ("malware.exe", file_content, "application/octet-stream")}

    response = client.post("/uploadFile", files=files)

    assert response.status_code == 403
    assert response.json()["detail"] == "Extension not allowed"


def test_upload_file_saves_correctly():
    file_content = b"Test file content"
    files = {"uploadedFile": ("example.txt", file_content, "text/plain")}

    response = client.post("/uploadFile", files=files)
    data = response.json()

    assert response.status_code == 200

    saved_path = os.path.join(data["file_location"], data["saved_as"])
    assert os.path.exists(saved_path)
    os.remove(saved_path)



def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
