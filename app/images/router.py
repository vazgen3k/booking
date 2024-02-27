from fastapi import UploadFile, APIRouter
from app.tasks.tasks import proccess_pic
import shutil

router = APIRouter(
    prefix="/images",
    tags=["загрузка картинок"])


@router.post('/hotels/')
async def add_hotel_image(name: int, file: UploadFile):
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    proccess_pic.delay(im_path)
