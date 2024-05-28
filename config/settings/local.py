
# Need to load this first so that env vars are loaded from .env before base.py is run
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # take environment variables from .env in local runserver

from .base import *


# Build paths inside the project like this: BASE_DIR / 'subdir'.


# take environment variables from .env in local runserver

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
DEBUG = True
ALLOWED_HOSTS = ['*']


MIDDLEWARE += []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
DB_NAME = os.environ.get("DB_NAME")
DB_PWD = os.environ.get("DB_PWD")
DB_USER = os.environ.get("DB_USER")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PWD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}
