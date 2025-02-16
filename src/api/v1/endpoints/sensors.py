from fastapi import APIRouter, HTTPException, Query, Request, status, Depends
from injector import Injector, inject
from service.file_service import MAX_FILE_SIZE, FileService

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
