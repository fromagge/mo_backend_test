import sys

# SECURITY WARNING: keep the secret key used in production secret!
from .base import *
import dj_database_url
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []

MIDDLEWARE += []



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
MAX_CONN_AGE = 600



# SSL / Security manage.py check --deploy --fail-level WARNING
# Intentionally don't redirect in CI environment.
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Set these when we're sure all page are SSL
# SECURE_HSTS_SECONDS = 3600  # 1 hour
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True



