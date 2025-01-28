from fastapi import APIRouter, File, UploadFile
from typing import Annotated

router = APIRouter()


class Sensor:
    def __init__(self, router: APIRouter):
        self.router = router

    @router.post("/uploadfile")
    async def create_upload_file(file: UploadFile | None = None):

        if not file:
            return {"message": "no file send"}
        else:
            return file
