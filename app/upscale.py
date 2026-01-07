import cv2
from cv2 import dnn_superres
import numpy as np
import base64
from config import MODEL_PATH
import uuid
import os

# Глобальная переменная для хранения экземпляра модели
scaler = None


def initialize_scaler(model_path = MODEL_PATH):
    """
    Загружаем модель и скейлер
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
    :return: Бинарные данные результата
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

    original_filename = f"{uuid.uuid4()}.{ext}"
    image_path = os.path.join(app.config['PROCESSED_FOLDER'], original_filename)

    cv2.imwrite(image_path, processed_image)

    return original_filename

    # # Преобразуем обработанное изображение обратно в бинарные данные
    # success, encoded_result = cv2.imencode(f".{ext}", processed_image)
    # if not success:
    #     raise ValueError(f"Ошибка кодирования изображения")
    #
    # # Возвращаем обработанное изображение в виде bytes
    # return encoded_result.tobytes()
