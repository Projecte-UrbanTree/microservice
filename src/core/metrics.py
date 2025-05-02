from prometheus_client import Gauge

soil_water_gauge = Gauge(
    "soil_water",
    "Soil water content",
    ["device_name", "dev_eui"],
)

soil_temp_gauge = Gauge(
    "soil_temp",
    "Soil temperature",
    ["device_name", "dev_eui"],
)

soil_ph_gauge = Gauge(
    "soil_ph",
    "Soil pH",
    ["device_name", "dev_eui"],
)
