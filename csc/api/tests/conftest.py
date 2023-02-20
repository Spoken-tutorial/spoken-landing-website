import os
import django
from django.conf import settings
import pytest

# We manually designate which settings we will be using in an environment variable
# This is similar to what occurs in the `manage.py`
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.config.settings')

def pytest_sessionstart(session):
    from django.test import TestCase
    TestCase.multi_db = True
    TestCase.databases = '__all__'


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': 'localhost',  # Empty for localhost through domain sockets.
        'PORT': '',  # Set to empty string for default.
    }

    settings.DATABASES['spk']: {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("SPOKEN_DB"),
        'USER': os.getenv("SPOKEN_DB_USER"),
        'PASSWORD': os.getenv("SPOKEN_DB_PASS"),
        'HOST': os.getenv("SPOKEN_DB_HOST"),
        'PORT': '', # Set to empty string for default.
    }

    settings.DATABASES['ers']: {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "ersdb", #os.getenv("ERS_DB"),
        'USER': "arj", #os.getenv("ERS_DB_USER"),
        'PASSWORD': "arj", #os.getenv("ERS_DB_PASS"),
        'HOST': "localhost", #os.getenv("ERS_DB_HOST"),
        'PORT':'', # Set to empty string for default.
    }
    settings.DATABASES['forums']: {	
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.	
        'NAME': os.getenv("FDB"),  # Or path to database file if using sqlite3.	
        'USER': os.getenv("FDB_USER"),	
        'PASSWORD': os.getenv("FDB_PASS"),
        'HOST': os.getenv("FDB_DB_HOST"), # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.	
        'PORT': '', # Set to empty string for default.
    }
    settings.DATABASES['moodle']: {	
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.	
        'NAME': os.getenv("MDL"), # Or path to database file if using sqlite3.	
        'USER': os.getenv("MDL_USER"),	
        'PASSWORD': os.getenv("MDL_PASS"),
        'HOST': os.getenv("MDL_DB_HOST"), # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.	
        'PORT': '',  # Set to empty string for default.	
    }
