import cv2
from cv2 import dnn_superres
from app.config import MODEL_PATH

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