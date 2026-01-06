import requests
import time
import base64
from app.config import INPUT_FOLDER, OUTPUT_FOLDER

BASE_URL = "http://127.0.0.1:5000"

# Передаем файл на обработку в POST запрос
with open(f"{INPUT_FOLDER}lama_300px.png", 'rb') as image:
    response = requests.post(f"{BASE_URL}/upscale/", files={
            'image': image
        })
    task_id = response.json()['task_id']
    print("Поставили задачу в Celery")
    print(f'{task_id=}')

# Ждем завершения обработки нашего файла
status = "WAIT..."
while status not in {"SUCCESS", "FAILURE"}:
    time.sleep(1.0)
    response = requests.get(f"{BASE_URL}/task/{task_id}")
    status = response.json()["status"]
    print(f'WAIT... {status}')

print(f'{status=}')

# Сохраняем преобразованный файл
if response.status_code == 200:
    print("Изображение успешно обработано, сохраняем...")
    # Получаем изображение из JSON как строку Base64
    base64_string = response.json()['result']
    # Декодируем Base64 строку в байты
    image_bytes = base64.b64decode(base64_string)
    # Сохраняем байтовую строку в файл
    with open(f"{OUTPUT_FOLDER}lama_600px.png", 'wb') as file:
        file.write(image_bytes)
    print("Обработанное изображение сохранено!")
else:
    print("Ошибка при загрузке изображения.")