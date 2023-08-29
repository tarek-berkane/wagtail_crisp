import os

import environ

from .base import *

# Change it to your config file path
config_file = "/home/coding43/config/crisp_blog"

env = environ.Env()
environ.Env.read_env(os.path.join(config_file, ".env"))


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

STATIC_ROOT = os.path.join(PUBLIC_DIR, "crisp_static")
STATIC_URL = "/crisp_static/"

MEDIA_ROOT = os.path.join(PUBLIC_DIR, "crisp_media")
MEDIA_URL = "/crisp_media/"


# settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {
            "read_default_file": os.path.join(config_file, "my.cnf"),
            "sql_mode": "traditional",
        },
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

REDIS_PAGE_STATICS_SERVICE_NAME = "codingdz:pages_statistics"


SILENCED_SYSTEM_CHECKS = [
    "captcha.recaptcha_test_key_error",
]

try:
    from .local import *
except ImportError:
    pass
