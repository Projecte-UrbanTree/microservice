import io
import os
import time
import shutil
from fastapi import APIRouter, HTTPException, Query, Request, status

router = APIRouter()

MAX_FILE_SIZE = 1024 * 1024  
DIR = "saved_files"
ALLOWED_EXTENSIONS = [".txt", ".json", ".csv"]

async def process_up(content: str, extension: str):
    print("Procesando evento 'up'")
    
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

    filename = f"{timestamp}{extension}"
    os.makedirs(DIR, exist_ok=True)
    file_location = os.path.join(DIR, filename)
    

    with open(file_location, "wb+") as f:
        shutil.copyfileobj(content, f)
    
    print(f"file saved: {file_location}")

async def process_join(content: str):
    pass

@router.post("/uploadFile")
async def create_upload_file(
    request: Request,
    event: str = Query(..., description="Tipo de evento. Ejemplo: 'up' o 'join'")
):
    body = await request.body()
    
    if (len(body) > MAX_FILE_SIZE):
        raise HTTPException(
            detail="File too large",
            status_code=403
        )
    
    content = io.BytesIO(body)
    
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    extension = ".json"
    filename = f"{timestamp}{extension}"
    os.makedirs(DIR, exist_ok=True)
    file_location = os.path.join(DIR, filename)

    with open(file_location, "wb") as f:
        f.write(content.getvalue())

    content.seek(0)

    if event == "up":
        await process_up(content, extension)
    elif event == "join":
        await process_join(content)
    else:
        raise HTTPException(status_code=400, detail=f"Evento {event} no implementado")

    return status.HTTP_200_OK
