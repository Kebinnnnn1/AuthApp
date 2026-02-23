web: python manage.py collectstatic --noinput && python manage.py migrate && python manage.py ensure_superuser && gunicorn django_auth.wsgi:application --bind 0.0.0.0:$PORT
