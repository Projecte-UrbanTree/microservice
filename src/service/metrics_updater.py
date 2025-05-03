from sqlalchemy import select, func
from sqlmodel import Session
from src.domain.entities.sensor_history import SensorHistory
from src.core.metrics import (
    soil_ph_gauge,
    soil_temp_gauge,
    soil_water_gauge,
    sensors_total,
    sensors_active,
    historical_records,
)

def update_sensor_metrics(
    sensor_data: list[dict],
    total_sensors: int,
    active_sensors: int,
    total_history_records: int,
):
    sensors_total.set(total_sensors)
    sensors_active.set(active_sensors)
    historical_records.set(total_history_records)

    for sensor in sensor_data:
        device_name = sensor.get("device_name", "unknown")
        dev_eui     = sensor.get("dev_eui",     "unknown")
        labels      = {"device_name": device_name, "dev_eui": dev_eui}

        if (w := sensor.get("water_soil")) is not None:
            soil_water_gauge.labels(**labels).set(w)
        if (t := sensor.get("temp_soil")) is not None:
            soil_temp_gauge.labels(**labels).set(t)
        if (p := sensor.get("ph1_soil")) is not None:
            soil_ph_gauge.labels(**labels).set(p)

def update_all_metrics(session: Session):
    """ Updates various sensor-related metrics by querying the database.

    This function performs the following operations:
      - Retrieves the total number of historical records from the database.
      - Calculates the total number of distinct sensors.
      - Determines the total number of active sensors (sensors with at least one record).
      - Fetches the latest data entry for each sensor and converts it into a list of dictionaries.

    The gathered metrics are then used to update the sensor metrics via the `update_sensor_metrics` function.

    Args:
        session (Session): The database session used to execute queries.

    Notes:
        - An "active sensor" is defined as a sensor with at least one record in the database.
        - The latest data for each sensor is determined by the maximum timestamp (`time`) for that sensor.
    """
    
    total_history = session.exec(
        select(func.count()).select_from(SensorHistory)
    ).one()

    total_sensors = session.exec(
        select(func.count(func.distinct(SensorHistory.dev_eui)))
    ).one()

    active_sensors = total_sensors

    subq = (
        select(
            SensorHistory.dev_eui,
            func.max(SensorHistory.time).label("max_time")
        )
        .group_by(SensorHistory.dev_eui)
        .subquery()
    )
    latest_q = (
        select(SensorHistory)
        .join(subq,
              (SensorHistory.dev_eui == subq.c.dev_eui)
              & (SensorHistory.time == subq.c.max_time))
    )
    results = session.exec(latest_q).all()
    latest_list = [r.model_dump() for r in results]

    update_sensor_metrics(
        sensor_data=latest_list,
        total_sensors=total_sensors,
        active_sensors=active_sensors,
        total_history_records=total_history,
    )