from flask import Flask
from flask import request
from flask.views import MethodView
from flask import jsonify
from celery_app import celery_app, get_task, upscale_image
from io import BytesIO
import base64

app = Flask('app')

class ContextTask(celery_app.Task):
    """
    Класс ContextTask переопределяет стандартный класс задач Celery.
    Цель переопределения заключается в обеспечении контекста Flask
    внутри задач Celery
    """
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = ContextTask


class UpscaleImage(MethodView):

    def get(self, task_id):
        task = get_task(task_id)
        result = task.result or b''

        # Конвертирование в Base64
        # результат работы задачи в Celery декодируется в строку
        # с использованием кодировки utf-8, чтобы его можно было вернуть в JSON.
        if isinstance(result, bytes):
            result = base64.b64encode(result).decode('utf-8')

        return jsonify({'status': task.status,
                        'result': result})


    def post(self):
        """
        Загружает изображение и ставит задачу на апскейлинг в Celery
        """

        if 'image' not in request.files:
            return jsonify({"error": "Отсутствует изображение"}), 400

        image = request.files['image']
        ext = image.filename.rsplit('.', 1)[1].lower()
        if ext not in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
            return jsonify({"error": "Неверный формат изображения"}), 400

        in_memory_file = BytesIO()
        image.save(in_memory_file) # Читаем содержимое файла сразу в память
        in_memory_file.seek(0)  # Сброс указателя в начало файла
        image_data = in_memory_file.read()  # Чтение данных из BytesIO

        try:
            task = upscale_image.delay(image_data, ext)  # Запускаем задачу в Celery
            return jsonify({"task_id": task.id, "status": "processing"}), 202
        except Exception as e:
            return jsonify({"error": str(e)}), 500

app.add_url_rule('/task/<string:task_id>',
                 view_func=UpscaleImage.as_view('task_status'),
                 methods=['GET']
                 )
app.add_url_rule('/upscale/',
                 view_func=UpscaleImage.as_view('upscale'),
                 methods=['POST']
                 )


if __name__ == '__main__':
    app.run()
