from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Text, JSON, text

class SensorHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deduplication_id: str = Field(..., max_length=100, sa_column_kwargs={"unique": True})
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
    tags: Optional[Dict[Any, Any]] = Field(default=None, sa_column=Column(JSON))
    
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
    phi_soil: Optional[float] = Field(default=None)
    
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
    modulation: Optional[Dict[Any, Any]] = Field(default=None, sa_column=Column(JSON))
    region_config_id: Optional[str] = Field(default=None, max_length=20)
    
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
