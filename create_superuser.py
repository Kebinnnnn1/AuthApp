"""
Auto-create superuser from environment variables on deploy.
Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD,
and optionally DJANGO_SUPERUSER_EMAIL in Railway env vars.
"""
import os
import django

# Force-set so it always works on Railway, never overridden by another env var
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_auth.settings'
django.setup()

from django.contrib.auth.models import User

# Strip whitespace in case it was accidentally copied with spaces in Railway
USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', '').strip()
PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '').strip()
EMAIL    = os.environ.get('DJANGO_SUPERUSER_EMAIL', '').strip()

if not USERNAME or not PASSWORD:
    print('ℹ️  DJANGO_SUPERUSER_USERNAME / PASSWORD not set — skipping superuser creation.')
elif User.objects.filter(username=USERNAME).exists():
    print(f'⚠️  User "{USERNAME}" already exists — skipping.')
else:
    User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
    print(f'✅ Superuser "{USERNAME}" created successfully!')
