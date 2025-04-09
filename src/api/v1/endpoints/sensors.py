from fastapi import APIRouter, HTTPException, Query, Request, status, Depends
from injector import Injector, inject
from src.service.file_service import MAX_FILE_SIZE, FileService
from sqlmodel import Session, select
from src.domain.entities.sensor_history import SensorHistory
from src.core.db.connection import get_session
from src.core.security.api_key import get_api_key
from typing import Optional, List
from datetime import datetime
from sqlalchemy import func

router = APIRouter()


def get_file_service(request: Request) -> FileService:
    injector: Injector = request.app.state.injector
    return injector.get(FileService)


@router.post("/uploadFile")
async def create_upload_file(
    request: Request,
    event: str = Query(...,
                       description="Tipo de evento. Ejemplo: 'up' o 'join'"),
    file_service: FileService = Depends(get_file_service),
):
    body = await request.body()

    if len(body) > MAX_FILE_SIZE:
        raise HTTPException(detail="File too large", status_code=403)

    extension = ".json"

    if event == "up":
        file_service.process_up(body, extension)
    elif event == "join":
        file_service.process_join(body)
    else:
        raise HTTPException(
            status_code=400, detail=f"Evento {event} no implementado")

    return status.HTTP_200_OK


@router.get("/sensors", response_model=list[SensorHistory])
def get_sensors(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    api_key: str = Depends(get_api_key)
):
    subq = (
        select(
            SensorHistory.dev_eui,
            func.max(SensorHistory.time).label("max_time")
        ).group_by(SensorHistory.dev_eui).subquery()
    )
    query = (
        select(SensorHistory)
        .join(
            subq,
            (SensorHistory.dev_eui == subq.c.dev_eui) & (
                SensorHistory.time == subq.c.max_time)
        )
        .offset(skip)
        .limit(limit)
    )
    return session.exec(query).all()


@router.get("/sensors/{sensor_id}", response_model=SensorHistory)
def get_sensor(
    sensor_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(get_api_key)
):
    sensor = session.get(SensorHistory, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.get("/sensors/deveui/{dev_eui}", response_model=SensorHistory)
def get_sensor_by_dev_eui(
    dev_eui: str,
    session: Session = Depends(get_session),
    api_key: str = Depends(get_api_key)
):
    sensor = session.exec(
        select(SensorHistory)
        .where(SensorHistory.dev_eui == dev_eui)
        .order_by(SensorHistory.time.desc())
    ).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.get("/sensors/deveui/{dev_eui}/history", response_model=List[SensorHistory])
def get_sensor_history(
    dev_eui: str,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    session: Session = Depends(get_session),
    api_key: str = Depends(get_api_key)
):

    query = select(SensorHistory).where(
        SensorHistory.dev_eui == dev_eui,
        (SensorHistory.check == None) | (SensorHistory.check == False)
    )

    if start_date:
        query = query.where(SensorHistory.time >= start_date)
    if end_date:
        query = query.where(SensorHistory.time <= end_date)

    if sort_order.lower() == "asc":
        query = query.order_by(SensorHistory.time.asc())
    else:
        query = query.order_by(SensorHistory.time.desc())

    results = session.exec(query.offset(skip).limit(limit)).all()

    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No sensor history found for device with dev_eui {dev_eui}"
        )

    return results


@router.post("/updateSensorHistory")
def update_sensor_history(
    ids: List[int],
    session: Session = Depends(get_session),
    api_key: str = Depends(get_api_key)
):
    records = session.exec(
        select(SensorHistory).where(SensorHistory.id.in_(ids))
    ).all()
    if not records:
        raise HTTPException(
            status_code=404, detail="No records found with provided IDs")
    for record in records:
        record.check = True
    session.commit()

    return {"updated": len(records), "ids": [record.id for record in records]}
