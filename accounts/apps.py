import os
from django.apps import AppConfig


def _create_superuser_from_env(sender, **kwargs):
    """
    Runs automatically after every `manage.py migrate`.
    Creates or updates the superuser from environment variables.
    This is guaranteed to run on Railway since migrations always run.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()

    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', '').strip()
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '').strip()
    email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', '').strip()

    print(f'[superuser] Checking env: USERNAME="{username}" PASSWORD={"SET" if password else "NOT SET"}')

    if not username or not password:
        print('[superuser] ⚠️  DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set. Skipping.')
        return

    try:
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.email        = email
        user.is_staff     = True
        user.is_superuser = True
        user.is_active    = True
        user.save()
        action = 'CREATED' if created else 'UPDATED'
        print(f'[superuser] ✅ Superuser "{username}" {action} — '
              f'is_staff={user.is_staff}, is_superuser={user.is_superuser}, is_active={user.is_active}')
    except Exception as e:
        print(f'[superuser] ❌ Failed to create/update superuser: {e}')


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(_create_superuser_from_env, sender=self)
