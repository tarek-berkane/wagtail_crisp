import os

import environ

from .base import *

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


DEBUG = False

SECRET_KEY = env("SECRET_KEY")


HOST = env("HOST")
ALLOWED_HOSTS = [
    HOST,
]

SECURE_SSL_REDIRECT = True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "log/output.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}



PUBLIC_DIR = env("PUBLIC_DIR")

STATIC_ROOT = os.path.join(PUBLIC_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(PUBLIC_DIR, "media")
MEDIA_URL = "/media/"


# settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {
            "read_default_file": os.path.join(BASE_DIR, "my.cnf"),
            'sql_mode': 'traditional',
        },
   }
}

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

try:
    from .local import *
except ImportError:
    pass
