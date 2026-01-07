from celery import Celery
from celery.result import AsyncResult
from upscale import upscale
from config import BROKER, BACKEND

celery_app = Celery("celery_app", backend=BACKEND, broker=BROKER)


def get_task(task_id: str) -> AsyncResult:
    return AsyncResult(task_id, app=celery_app)


@celery_app.task
def upscale_image(image: bytes, ext: str):
    result = upscale(image, ext)
    return result
