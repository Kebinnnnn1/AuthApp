from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Create or update superuser from environment variables'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', '').strip()
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '').strip()
        email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', '').strip()

        self.stdout.write(f'[superuser] USERNAME = "{username}"')
        self.stdout.write(f'[superuser] EMAIL    = "{email}"')
        self.stdout.write(f'[superuser] PASSWORD = {"SET" if password else "NOT SET"}')

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                '[superuser] ❌ DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set — skipping.'
            ))
            return

        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.email        = email
        user.is_staff     = True
        user.is_superuser = True
        user.is_active    = True
        user.save()

        action = 'created' if created else 'updated'
        self.stdout.write(self.style.SUCCESS(
            f'[superuser] ✅ Superuser "{username}" {action} — '
            f'is_staff={user.is_staff}, is_superuser={user.is_superuser}, is_active={user.is_active}'
        ))
