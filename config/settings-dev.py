from .settings import *

DEBUG = True

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "referal",
        "USER": "alexmaurus",
        "PASSWORD": "1",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
