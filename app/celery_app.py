import uuid
import os
from celery import Celery
from celery.result import AsyncResult
from upscale import upscale, upscale2
from config import BROKER, BACKEND, PROCESS_FOLDER

celery_app = Celery("celery_app", backend=BACKEND, broker=BROKER)


def get_task(task_id: str) -> AsyncResult:
    return AsyncResult(task_id, app=celery_app)


# @celery_app.task
# def upscale_image(image_path):
#     ext = image_path.rsplit('.', 1)[1].lower()
#     new_filename = f"{uuid.uuid4()}_upscaled.{ext}"
#     new_file_path = os.path.join(PROCESS_FOLDER, new_filename)
#     upscale(image_path, new_file_path)
#     return new_filename

@celery_app.task
def upscale_image(image: bytes, ext: str):
    # ext = image_path.rsplit('.', 1)[1].lower()
    # new_filename = f"{uuid.uuid4()}_upscaled.{ext}"
    # new_file_path = os.path.join(PROCESS_FOLDER, new_filename)
    result = upscale2(image, ext)
    return result