"""
Auto-create OR fix superuser on every Railway deploy.
Always ensures the superuser has correct credentials + permissions.

Required Railway env vars:
  DJANGO_SUPERUSER_USERNAME
  DJANGO_SUPERUSER_PASSWORD
  DJANGO_SUPERUSER_EMAIL  (optional)
"""
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_auth.settings'
django.setup()

from django.contrib.auth.models import User

USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', '').strip()
PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '').strip()
EMAIL    = os.environ.get('DJANGO_SUPERUSER_EMAIL', '').strip()

print(f'[superuser] USERNAME env = "{USERNAME}"')
print(f'[superuser] EMAIL env    = "{EMAIL}"')
print(f'[superuser] PASSWORD set = {"YES" if PASSWORD else "NO"}')

if not USERNAME or not PASSWORD:
    print('[superuser] ❌ DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD is not set — skipping.')
else:
    user, created = User.objects.get_or_create(username=USERNAME)

    # Always sync password, email, and permissions regardless of whether just created
    user.set_password(PASSWORD)
    user.email       = EMAIL
    user.is_staff    = True
    user.is_superuser = True
    user.is_active   = True
    user.save()

    if created:
        print(f'[superuser] ✅ Superuser "{USERNAME}" created with full permissions.')
    else:
        print(f'[superuser] ✅ Superuser "{USERNAME}" already existed — password + permissions synced.')

    # Confirm final state in logs
    u = User.objects.get(username=USERNAME)
    print(f'[superuser] Final state → is_staff={u.is_staff}, is_superuser={u.is_superuser}, is_active={u.is_active}')
