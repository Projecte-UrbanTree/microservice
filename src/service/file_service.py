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
        """Converts JSON data to a SensorHistory entity"""
        sensor_history = SensorHistory(
            deduplication_id=json_data.get("deduplicationId", ""),
            time=datetime.fromisoformat(json_data.get(
                "time", "").replace("Z", "+00:00"))
        )

        # Device information processing
        if device_info := json_data.get("deviceInfo"):
            sensor_history.tenant_id = device_info.get("tenantId")
            sensor_history.tenant_name = device_info.get("tenantName")
            sensor_history.application_id = device_info.get("applicationId")
            sensor_history.application_name = device_info.get(
                "applicationName")
            sensor_history.device_profile_id = device_info.get(
                "deviceProfileId")
            sensor_history.device_profile_name = device_info.get(
                "deviceProfileName")
            sensor_history.device_name = device_info.get("deviceName")
            sensor_history.dev_eui = device_info.get("devEui")
            sensor_history.device_class_enabled = device_info.get(
                "deviceClassEnabled")
            sensor_history.tags = device_info.get("tags")

        # Transmission info
        sensor_history.dev_addr = json_data.get("devAddr")
        sensor_history.adr = json_data.get("adr")
        sensor_history.dr = json_data.get("dr")
        sensor_history.f_cnt = json_data.get("fCnt")
        sensor_history.f_port = json_data.get("fPort")
        sensor_history.confirmed = json_data.get("confirmed")
        sensor_history.data = json_data.get("data")

        # Sensor measurements
        if obj_data := json_data.get("object"):
            sensor_history.message_type = obj_data.get("Message_type")
            sensor_history.bat = obj_data.get("Bat")
            sensor_history.tempc_ds18b20 = self._parse_float(
                obj_data.get("TempC_DS18B20"))
            sensor_history.temp_soil = self._parse_float(
                obj_data.get("TEMP_SOIL"))
            sensor_history.interrupt_flag = obj_data.get("Interrupt_flag")
            sensor_history.phi_soil = self._parse_float(
                obj_data.get("PH_SOIL"))

        # Reception information
        if rx_info := json_data.get("rxInfo", []):
            if rx_info and len(rx_info) > 0:
                first_rx = rx_info[0]
                sensor_history.gateway_id = first_rx.get("gatewayId")
                sensor_history.uplink_id = first_rx.get("uplinkId")
                sensor_history.gw_time = datetime.fromisoformat(first_rx.get(
                    "gwTime", "").replace("Z", "+00:00")) if first_rx.get("gwTime") else None
                sensor_history.rssi = first_rx.get("rssi")
                sensor_history.snr = first_rx.get("snr")
                sensor_history.channel = first_rx.get("channel")
                sensor_history.rf_chain = first_rx.get("rxChain")

                if location := first_rx.get("location"):
                    sensor_history.latitude = location.get("latitude")
                    sensor_history.longitude = location.get("longitude")

                sensor_history.context = first_rx.get("context")
                sensor_history.crc_status = first_rx.get("crcStatus")

        # TX information
        if tx_info := json_data.get("txInfo"):
            sensor_history.frequency = tx_info.get("frequency")
            sensor_history.modulation = tx_info.get("modulation")

        sensor_history.region_config_id = json_data.get("regionConfigId")

        return sensor_history

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
