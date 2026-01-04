import cv2
from cv2 import dnn_superres

# Загружаем модель и скейлер при старте
scaler = dnn_superres.DnnSuperResImpl_create()
scaler.readModel('models/EDSR_x2.pb')
scaler.setModel("edsr", 2)

def upscale(input_path: str, output_path: str) -> None:
    """
    Апскейлинг изображения.
    :param input_path: путь к входному изображению
    :param output_path: путь к выходному изображению
    :return:
    """

    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)
