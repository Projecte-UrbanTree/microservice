from fastapi import APIRouter, HTTPException, Query, Request, status, Depends
from injector import Injector, inject
from src.service.file_service import MAX_FILE_SIZE, FileService
from sqlmodel import Session, select
from src.domain.entities.sensor_history import SensorHistory
from src.core.db.connection import get_session

router = APIRouter()


def get_file_service(request: Request) -> FileService:
    injector: Injector = request.app.state.injector
    return injector.get(FileService)


@router.post("/uploadFile")
async def create_upload_file(
    request: Request,
    event: str = Query(...,
                       description="Tipo de evento. Ejemplo: 'up' o 'join'"),
    file_service: FileService = Depends(get_file_service)
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
def get_sensors(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return session.exec(select(SensorHistory).offset(skip).limit(limit)).all()


@router.get("/sensors/{sensor_id}", response_model=SensorHistory)
def get_sensor(sensor_id: int, session: Session = Depends(get_session)):
    sensor = session.get(SensorHistory, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor
