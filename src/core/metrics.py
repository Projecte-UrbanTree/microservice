from prometheus_client import Gauge

#Global metrics
sensors_total = Gauge(
    "microservice_test_sensors_total",
    "Total number of sensors in the database",
)

sensors_active = Gauge(
    "microservice_test_sensors_active",
    "Number of sensors with datos recientes (último dato)",
)

historical_records = Gauge(
    "microservice_test_historical_records_total",
    "Total number of historical records in the database",
)

# Sensor metrics
soil_water_gauge = Gauge("microservice_test_soil_water", "Soil water content", ["device_name","dev_eui"])
soil_temp_gauge  = Gauge("microservice_test_soil_temp" , "Soil temperature"  , ["device_name","dev_eui"])
soil_ph_gauge    = Gauge("microservice_test_soil_ph"   , "Soil pH"          , ["device_name","dev_eui"])