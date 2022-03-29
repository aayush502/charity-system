web: gunicorn charity_management.wsgi
worker: celery -A charity_management worker --beat -S django --l info