import os
import time
import json
from datetime import datetime
from sqlmodel import Session
from src.domain.entities.sensor_history import SensorHistory

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
        try:
            json_data = json.loads(content.decode('utf-8'))
            sensor_data = self._convert_to_sensor_history(json_data)
            self._save_to_database(sensor_data)
        except Exception as e:
            print(f"Error processing file: {e}")

    def process_join(self, content: bytes):
        file_location = self.save_file(content, ".json")
        try:
            json_data = json.loads(content.decode('utf-8'))
            sensor_data = self._convert_to_sensor_history(json_data)
            self._save_to_database(sensor_data)
        except Exception as e:
            print(f"Error processing join file: {e}")

    def _convert_to_sensor_history(self, json_data: dict) -> SensorHistory:
        return SensorHistory.from_json(json_data)

    def _parse_float(self, value):
        """Safely converts a string to float"""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def _save_to_database(self, sensor_data: SensorHistory):
        """Saves the SensorHistory entity to the database"""
        try:
            self.session.add(sensor_data)
            self.session.commit()
            print(f"Data saved to database with ID: {sensor_data.id}")
        except Exception as e:
            self.session.rollback()
            print(f"Error saving to database: {e}")
