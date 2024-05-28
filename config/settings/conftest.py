import pytest
from django.conf import settings
from django.apps import apps
from django.db import connection

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
        'TEST': {
            'NAME': 'test_db',
        },
    }

    load_test_models()

    # Yield to run the test setup
    yield


def load_test_models():
    # Define the models you want to load
    models_to_load = ['app1.Model1', 'app2.Model2']

    for model_name in models_to_load:
        try:
            # Get the model class
            model_class = apps.get_model(model_name)

            # Ensure the model is synchronized with the database schema
            if not model_class._meta.db_table in connection.introspection.table_names():
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(model_class)

        except LookupError:
            print(f"Model '{model_name}' not found.")