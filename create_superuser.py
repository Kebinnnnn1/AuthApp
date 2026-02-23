"""
Auto-create superuser from environment variables on deploy.
Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD,
and optionally DJANGO_SUPERUSER_EMAIL in Railway env vars.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_auth.settings')
django.setup()

from django.contrib.auth.models import User

USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', '')
PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')

if not USERNAME or not PASSWORD:
    print('ℹ️  DJANGO_SUPERUSER_USERNAME / PASSWORD not set — skipping superuser creation.')
elif User.objects.filter(username=USERNAME).exists():
    print(f'⚠️  User "{USERNAME}" already exists — skipping.')
else:
    User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
    print(f'✅ Superuser "{USERNAME}" created successfully!')
