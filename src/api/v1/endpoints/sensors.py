import os
from fastapi import APIRouter, UploadFile, HTTPException
import time
import shutil

router = APIRouter()

MAX_FILE = 1024 * 1024
DIR = "saved_files"
ALLOWED_EXTENSIONS = [".txt", ".json", ".csv"]


@router.post("/uploadFile")
async def create_upload_file(uploadedFile: UploadFile):
    if uploadedFile.size > MAX_FILE:
        raise HTTPException(
            status_code=403,
            detail="File too large",
        )

    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    extension = os.path.splitext(uploadedFile.filename)[1]

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=403, detail="Extension not allowed")

    filename = f"{timestamp}{extension}"
    os.makedirs(DIR, exist_ok=True)

    file_location = os.path.join(DIR, filename)

    with open(file_location, "wb+") as f:
        shutil.copyfileobj(uploadedFile.file, f)

    return {
        "filename": uploadedFile.filename,
        "saved_as": filename,
        "file_location": os.path.dirname(file_location),
    }
