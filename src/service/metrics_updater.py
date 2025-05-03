from src.core.metrics import soil_ph_gauge, soil_temp_gauge, soil_water_gauge


def update_sensor_metrics(sensor_data: list[dict]):
    for sensor in sensor_data:
        soil_water = sensor.get("water_soil")
        soil_temp = sensor.get("temp_soil")
        soil_ph = sensor.get("ph1_soil")
        device_name = sensor.get("device_name", "unknown")
        dev_eui = sensor.get("dev_eui", "unknown")
        labels = {"device_name": device_name, "dev_eui": dev_eui}

        if soil_water is not None:
            soil_water_gauge.labels(**labels).set(soil_water)
        if soil_temp is not None:
            soil_temp_gauge.labels(**labels).set(soil_temp)
        if soil_ph is not None:
            soil_ph_gauge.labels(**labels).set(soil_ph)
