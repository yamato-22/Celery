import cv2
from cv2 import dnn_superres
import numpy as np
from config import MODEL_PATH

# Глобальная переменная для хранения экземпляра модели
scaler = None


def initialize_scaler(model_path = MODEL_PATH):
    """
    # Загружаем модель и скейлер
    """

    global scaler
    if scaler is None:
        scaler = dnn_superres.DnnSuperResImpl_create()
        scaler.readModel(model_path)
        scaler.setModel("edsr", 2)


def upscale(input_path: str, output_path: str) -> None:
    """
    :param input_path: путь к изображению для апскейла
    :param output_path: путь к выходному файлу
    :return:
    """
    # Проверяем, была ли модель уже инициализирована
    if scaler is None:
        initialize_scaler()

    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)


def upscale2(input_data: bytes, ext="jpg") -> bytes:
    """
    Апскейлинг изображения без записи на диск.

    :param input_data: Входящие бинарные данные изображения
    :param output_format: Формат вывода (.jpg, .png и др.)
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
    result = scaler.upsample(image)

    # Кодируем результат обратно в поток байтов
    success, encoded_result = cv2.imencode(f".{ext}", result)
    if not success:
        raise ValueError(f"Ошибка кодирования изображения")

    # Возвращаем результат в виде байтового потока
    return encoded_result.tobytes()