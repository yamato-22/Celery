import requests
import time
import base64
from app.config import INPUT_FOLDER, OUTPUT_FOLDER

BASE_URL = "http://127.0.0.1:5000"
image_filename='lama_300px.png'

def save_image(filename: str, image_data: bytes):
    image_bytes = base64.b64decode(image_data)
    ext = filename.rsplit('.', 1)[1].lower()
    new_filename = f'{filename.split('.')[0]}_upscaled.{ext}'
    with open(f"{OUTPUT_FOLDER}{new_filename}", 'wb') as file:
        file.write(image_bytes)
    print("Обработанное изображение сохранено!")

# Передаем файл на обработку в POST запрос
with open(f"{INPUT_FOLDER}{image_filename}", 'rb') as image:
    response = requests.post(f"{BASE_URL}/upscale/", files={
            'image': image
        })
    task_id = response.json()['task_id']
    print("Поставили задачу в Celery на выполнение")
    # print(f'{task_id=}')

# Ждем завершения обработки нашего файла
status = "WAIT..."
while status not in {"SUCCESS", "FAILURE"}:
    time.sleep(1.0)
    response = requests.get(f"{BASE_URL}/task/{task_id}")
    status = response.json()["status"]
    print(f'WAIT... {status}')

print(f'{status=}')

# Сохраняем преобразованный файл из данных ответа POST запроса.
if response.status_code == 200:
    print("Изображение успешно обработано, сохраняем...")
    # Получаем изображение из JSON как строку Base64
    base64_string = response.json()['result']
    # Сохраняем полученное изображение
    save_image(image_filename, base64_string)

#     # Декодируем Base64 строку в байты
#     image_bytes = base64.b64decode(base64_string)
#     # Сохраняем байтовую строку в файл
#     ext = image_filename.rsplit('.', 1)[1].lower()
#     new_filename = f'{image_filename.split('.')[0]}_upscaled.{ext}'
#     with open(f"{OUTPUT_FOLDER}{new_filename}", 'wb') as file:
#         file.write(image_bytes)
#     print("Обработанное изображение сохранено!")
# else:
#     print("Ошибка при загрузке изображения.")

