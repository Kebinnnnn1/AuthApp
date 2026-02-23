"""
Django settings for django_auth project.
"""

import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production-xyz123abc456')

DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_auth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_auth.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth redirects
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ─────────────────────────────────────────────
# EMAIL CONFIGURATION
# ─────────────────────────────────────────────
# Uses SMTP if EMAIL_HOST_USER / EMAIL_HOST_PASSWORD env vars are set.
# Otherwise falls back to console backend (codes print in the terminal).
#
# To enable Gmail SMTP, run these in PowerShell before `python manage.py runserver`:
#   $env:EMAIL_HOST_USER     = "you@gmail.com"
#   $env:EMAIL_HOST_PASSWORD = "your-16-char-app-password"
#
_smtp_user = os.environ.get('EMAIL_HOST_USER', '')
_smtp_pass = os.environ.get('EMAIL_HOST_PASSWORD', '')

if _smtp_user and _smtp_pass:
    EMAIL_BACKEND    = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST       = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT       = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS    = True
    EMAIL_HOST_USER  = _smtp_user
    EMAIL_HOST_PASSWORD = _smtp_pass
    DEFAULT_FROM_EMAIL  = f'AuthApp <{_smtp_user}>'
else:
    # Development — code prints in runserver terminal
    EMAIL_BACKEND      = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'AuthApp <noreply@authapp.local>'
