import uuid
import os

from flask import Flask
from flask import request
from flask.views import MethodView
from flask import jsonify
from flask import send_file
from celery_app import celery_app, get_task, upscale_image
from config import UPLOAD_FOLDER, PROCESS_FOLDER

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
        return jsonify({'status': task.status,
                        'result': task.result})

    def post(self):
        """Загружает изображение и ставит задачу на апскейлинг"""
        if 'image' not in request.files:
            return jsonify({"error": "Отсутствует изображение"}), 400

        image = request.files['image']
        ext = image.filename.rsplit('.', 1)[1].lower()
        if ext not in ['jpg', 'jpeg', 'png']:
            return jsonify({"error": "Неверный формат изображения"}), 400

        original_filename = f"{uuid.uuid4()}.{ext}"
        image_path = os.path.join(UPLOAD_FOLDER, original_filename)
        image.save(image_path)

        task = upscale_image.delay(image_path)
        return jsonify({"task_id": task.id, "upscale_file": task.result}), 202

class GetImage(MethodView):

    def get(self, filename):
        """Возвращает готовое апскейлированное изображение"""
        processed_path = os.path.join(PROCESS_FOLDER, filename)
        print(processed_path)
        if os.path.exists(processed_path):
            return send_file(processed_path, mimetype='image/jpeg')
        else:
            return jsonify({'message': 'Processed image not found.'}), 404

app.add_url_rule('/task/<string:task_id>',
                 view_func=UpscaleImage.as_view('task_status'),
                 methods=['GET']
                 )
app.add_url_rule('/processed/<string:filename>',
                 view_func=GetImage.as_view('processed_image'),
                 methods=['GET']
                 )
app.add_url_rule('/upscale/',
                 view_func=UpscaleImage.as_view('upscale'),
                 methods=['POST']
                 )


if __name__ == '__main__':
    app.run()
