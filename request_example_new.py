import requests
import time

IMAGES_FOLDER = "app/files/"
BASE_URL = "http://127.0.0.1:5000"

# Передаем файл на обработку в Celery
with open(f"{IMAGES_FOLDER}lama_300px.png", 'rb') as image:
    response = requests.post(f"{BASE_URL}/upscale/", files={
            'image': image
        })
    print(response.json())
    task_id = response.json()['task_id']

# Ждем завершения обработки нашего файла
status = "WAIT..."
while status not in {"SUCCESS", "FAILURE"}:
    time.sleep(1.0)
    response = requests.get(f"{BASE_URL}/task/{task_id}").json()
    status = response["status"]
    # result = response["result"]
    print(f'WAIT... {status}')

print(f'{status=}')

if response.status_code == 200:
    # Сохраняем изображение на диск
    with open(f"{IMAGES_FOLDER}lama_600px.png", 'wb') as file:
        file.write(response.content)
    print("Изображение успешно сохранено!")
else:
    print("Ошибка при загрузке изображения.")
# print(f'Upscaled file: {result=}')

# # Получаем преобразованный файл
# response = requests.get(f"{BASE_URL}/processed/{result}")
# print(response.status_code)
# if response.status_code == 200:
#     with open(f"{IMAGES_FOLDER}lama_600px.png", 'wb') as f:
#         f.write(response.content)