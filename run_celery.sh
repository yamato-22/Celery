cd app
celery -A celery_app.celery_app worker -c 4
