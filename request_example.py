import requests
import time
from app.config import INPUT_FOLDER, OUTPUT_FOLDER

BASE_URL = "http://127.0.0.1:5000"
image_filename = 'cat_500px.jpg'

# Передаем файл на обработку в POST запрос
with open(f"{INPUT_FOLDER}{image_filename}", 'rb') as image:
    response = requests.post(f"{BASE_URL}/upscale/", files={
            'image': image
        })
    task_id = response.json()['task_id']
    print("Поставили задачу в Celery на выполнение")

# Ждем завершения обработки нашего файла
status = "WAIT..."
while status not in {"SUCCESS", "FAILURE"}:
    time.sleep(1.0)
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    status = response.json()["status"]
    print(f'WAIT... {status}')

print(f'{status=}')

# Сохраняем преобразованный файл из данных ответа POST запроса.
if response.status_code == 200:
    print("Изображение успешно обработано, сохраняем...")

    link = response.json()['url']
    ext = image_filename.rsplit('.', 1)[1].lower()
    new_filename = f'{image_filename.split('.')[0]}_upscaled.{ext}'

    # Получаем преобразованный файл
    response = requests.get(f"{BASE_URL}{link}")
    if response.status_code == 200:
        with open(f'{OUTPUT_FOLDER}{new_filename}', 'wb') as f:
            f.write(response.content)
        print("Обработанное изображение сохранено!")
    else:
        print(f'{response.status_code=}')
        print(response.json()['message'])
