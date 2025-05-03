from prometheus_client import Gauge, Counter

unique_sensors_gauge = Gauge(
    "microservice_unique_sensors_total",
    "Total number of unique sensors",
)

sensor_data_counter = Counter(
    "microservice_sensor_data_received_total",
    "Total number of sensor data points received",
)

soil_water_gauge = Gauge(
    "microservice_soil_water",
    "Soil water content",
    ["device_name", "dev_eui"],
)

soil_temp_gauge = Gauge(
    "microservice_soil_temp",
    "Soil temperature",
    ["device_name", "dev_eui"],
)

soil_ph_gauge = Gauge(
    "microservice_soil_ph",
    "Soil pH",
    ["device_name", "dev_eui"],
)
