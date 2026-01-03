import requests
import time

# Передаем файл на обработку в Celery
with open("app/files/lama_300px.png", 'rb') as image:
    response = requests.post("http://127.0.0.1:5000/upscale/", files={
            'image': image
        })
    task_id = response.json()['task_id']

# Ждем завершения обработки нашего файла
status = "WAITING"
while status not in {"SUCCESS", "FAILURE"}:
    time.sleep(1.0)
    response = requests.get(f"http://127.0.0.1:5000/task/{task_id}").json()
    status = response["status"]
    result = response["result"]
    print(status)

print(f'{status=}')
print(f'{result=}')

# Получаем преобразованный файл
response = requests.get(f"http://127.0.0.1:5000/processed/{result}")
print(response.status_code)
if response.status_code == 200:
    with open("app/files/new_lama_600px.png", 'wb') as f:
        f.write(response.content)