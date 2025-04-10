from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field, Boolean
from sqlalchemy import Column, DateTime, Text, JSON, text


class SensorHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deduplication_id: str = Field(..., max_length=100, sa_column_kwargs={
        "unique": True})
    time: datetime

    tenant_id: Optional[str] = Field(default=None, max_length=50)
    tenant_name: Optional[str] = Field(default=None, max_length=100)
    application_id: Optional[str] = Field(default=None, max_length=50)
    application_name: Optional[str] = Field(default=None, max_length=100)
    device_profile_id: Optional[str] = Field(default=None, max_length=50)
    device_profile_name: Optional[str] = Field(default=None, max_length=100)
    device_name: Optional[str] = Field(default=None, max_length=100)
    dev_eui: Optional[str] = Field(default=None, max_length=50)
    device_class_enabled: Optional[str] = Field(default=None, max_length=20)
    tags: Optional[Dict[Any, Any]] = Field(
        default=None, sa_column=Column(JSON))

    dev_addr: Optional[str] = Field(default=None, max_length=20)
    adr: Optional[bool] = Field(default=None)
    dr: Optional[int] = Field(default=None)
    f_cnt: Optional[int] = Field(default=None)
    f_port: Optional[int] = Field(default=None)
    confirmed: Optional[bool] = Field(default=None)
    data: Optional[str] = Field(default=None, sa_column=Column(Text))

    message_type: Optional[int] = Field(default=None)
    water_soil: Optional[float] = Field(default=None)
    conductor_soil: Optional[int] = Field(default=None)
    temp_soil: Optional[float] = Field(default=None)
    bat: Optional[float] = Field(default=None)
    tempc_ds18b20: Optional[float] = Field(default=None)
    interrupt_flag: Optional[int] = Field(default=None)
    ph1_soil: Optional[float] = Field(default=None)

    gateway_id: Optional[str] = Field(default=None, max_length=50)
    uplink_id: Optional[int] = Field(default=None)
    gw_time: Optional[datetime] = Field(default=None)
    rssi: Optional[int] = Field(default=None)
    snr: Optional[float] = Field(default=None)
    channel: Optional[int] = Field(default=None)
    rf_chain: Optional[int] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    context: Optional[str] = Field(default=None, max_length=50)
    crc_status: Optional[str] = Field(default=None, max_length=20)

    frequency: Optional[int] = Field(default=None)
    modulation: Optional[Dict[Any, Any]] = Field(
        default=None, sa_column=Column(JSON))
    region_config_id: Optional[str] = Field(default=None, max_length=20)

    check: Optional[bool] = Field(default=False, sa_column=Column(
        Boolean, server_default=text("false")))

    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime,
            server_default=text("CURRENT_TIMESTAMP"),
            onupdate=text("CURRENT_TIMESTAMP")
        )
    )

    @classmethod
    def from_json(cls, json_data: dict) -> "SensorHistory":
        from datetime import datetime
        instance = cls(
            deduplication_id=json_data.get("deduplicationId", ""),
            time=datetime.fromisoformat(json_data.get(
                "time", "").replace("Z", "+00:00"))
        )
        # Map deviceInfo
        device_info = json_data.get("deviceInfo", {})
        instance.tenant_id = device_info.get("tenantId")
        instance.tenant_name = device_info.get("tenantName")
        instance.application_id = device_info.get("applicationId")
        instance.application_name = device_info.get("applicationName")
        instance.device_profile_id = device_info.get("deviceProfileId")
        instance.device_profile_name = device_info.get("deviceProfileName")
        instance.device_name = device_info.get("deviceName")
        instance.dev_eui = device_info.get("devEui")
        instance.device_class_enabled = device_info.get("deviceClassEnabled")
        instance.tags = device_info.get("tags")

        # Transmission info
        instance.dev_addr = json_data.get("devAddr")
        instance.adr = json_data.get("adr")
        instance.dr = json_data.get("dr")
        instance.f_cnt = json_data.get("fCnt")
        instance.f_port = json_data.get("fPort")
        instance.confirmed = json_data.get("confirmed")
        instance.data = json_data.get("data")

        # Sensor measurements
        obj_data = json_data.get("object", {})
        instance.message_type = obj_data.get("Message_type")
        instance.bat = obj_data.get("Bat")
        instance.tempc_ds18b20 = cls._parse_float(
            obj_data.get("TempC_DS18B20"))
        instance.temp_soil = cls._parse_float(obj_data.get("temp_SOIL"))
        instance.water_soil = cls._parse_float(obj_data.get("water_SOIL"))
        instance.conductor_soil = cls._parse_float(
            obj_data.get("conduct_SOIL"))
        instance.interrupt_flag = obj_data.get("Interrupt_flag")
        instance.ph1_soil = cls._parse_float(obj_data.get("PH1_SOIL"))

        # Reception info
        rx_info = json_data.get("rxInfo", [])
        if rx_info:
            first_rx = rx_info[0]
            instance.gateway_id = first_rx.get("gatewayId")
            instance.uplink_id = first_rx.get("uplinkId")
            gw_time = first_rx.get("gwTime")
            instance.gw_time = datetime.fromisoformat(
                gw_time.replace("Z", "+00:00")) if gw_time else None
            instance.rssi = first_rx.get("rssi")
            instance.snr = first_rx.get("snr")
            instance.channel = first_rx.get("channel")
            instance.rf_chain = first_rx.get("rxChain")
            location = first_rx.get("location", {})
            instance.latitude = location.get("latitude")
            instance.longitude = location.get("longitude")
            instance.context = first_rx.get("context")
            instance.crc_status = first_rx.get("crcStatus")

        # TX information
        tx_info = json_data.get("txInfo", {})
        instance.frequency = tx_info.get("frequency")
        instance.modulation = tx_info.get("modulation")

        instance.region_config_id = json_data.get("regionConfigId")
        return instance

    @staticmethod
    def _parse_float(value):
        try:
            return float(value) if value is not None else None
        except (ValueError, TypeError):
            return None
