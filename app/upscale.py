import uuid
import os
import cv2
from cv2 import dnn_superres
import numpy as np
from config import MODEL_PATH, PROCESSED_FOLDER


# Глобальная переменная для хранения экземпляра модели
scaler = None


def initialize_scaler(model_path=MODEL_PATH):
    """
    Функция обеспечивает однократную инициализацию модели EDSR

    :param model_path: путь к файлу модели
    """

    global scaler

    if scaler is None:
        scaler = dnn_superres.DnnSuperResImpl_create()
        scaler.readModel(model_path)
        scaler.setModel("edsr", 2)


def upscale(input_data: bytes, ext="jpg"):
    """
    Апскейлинг изображения без записи на диск.

    :param input_data: Входящие бинарные данные изображения
    :param ext: Формат вывода (.jpg, .png и др.)
    :return: Имя файла полученного изображения
    """

    # Преобразуем бинарные данные в массив NumPy
    nparray = np.frombuffer(input_data, dtype=np.uint8)

    # Декодируем изображение из потока байтов
    image = cv2.imdecode(nparray, flags=cv2.IMREAD_COLOR)

    # Инициализация модели, если ещё не сделана
    if scaler is None:
        initialize_scaler()

    # Масштабирование изображения
    processed_image = scaler.upsample(image)

    # Сохранение обработанного изображения
    original_filename = f"{uuid.uuid4()}.{ext}"
    image_path = os.path.join(PROCESSED_FOLDER, original_filename)
    cv2.imwrite(image_path, processed_image)

    return original_filename
