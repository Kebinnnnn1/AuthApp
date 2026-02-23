web: python manage.py collectstatic --noinput && python manage.py migrate && python create_superuser.py && gunicorn django_auth.wsgi:application --bind 0.0.0.0:$PORT
