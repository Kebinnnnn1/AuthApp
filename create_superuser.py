"""
One-time script to create the initial superuser.
Run with: python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_auth.settings')
django.setup()

from django.contrib.auth.models import User

USERNAME = 'Kebiinnnnn'
PASSWORD = 'Villaro1'
EMAIL = ''

if User.objects.filter(username=USERNAME).exists():
    print(f'⚠️  User "{USERNAME}" already exists — skipping.')
else:
    User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
    print(f'✅ Superuser "{USERNAME}" created successfully!')
