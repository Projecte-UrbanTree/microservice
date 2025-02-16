import os
import time
from sqlmodel import Session

DIR = "saved_files"
MAX_FILE_SIZE = 1024 * 1024
ALLOWED_EXTENSIONS = [".txt", ".json", ".csv"]


class FileService:
    def __init__(self, session: Session):
        self.session = session

    def save_file(self, content: bytes, extension: str) -> str:
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        filename = f"{timestamp}{extension}"
        os.makedirs(DIR, exist_ok=True)
        file_location = os.path.join(DIR, filename)

        with open(file_location, "wb") as f:
            f.write(content)

        return file_location

    def process_up(self, content: bytes, extension: str):
        file_location = self.save_file(content, extension)

    def process_join(self, content: bytes):
        pass
