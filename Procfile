release: python manage.py migrate --no-input
web: daphne config.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: celery -A config worker -l info --concurrency 1