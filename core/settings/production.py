import os
import environ

from .base import *

os.environ.setdefault("config_folder", "/home/config/")
config_file = os.environ.get("config_folder")


env = environ.Env()
environ.Env.read_env(os.path.join(config_file, ".env"))


DEBUG = False

SECRET_KEY = env("secret_key")


HOST = env("host")
ALLOWED_HOSTS = [HOST]

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


PUBLIC_DIR = env("public_dir")

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
            "charset": "utf8mb4",
        },
    }
}

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     }
# }

# REDIS_PAGE_STATICS_SERVICE_NAME = "codingdz:pages_statistics"


SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]

RECAPTCHA_PUBLIC_KEY = env("recaptch_public_key")
RECAPTCHA_PRIVATE_KEY = env("recaptcha_private_key")


try:
    from .local import *
except ImportError:
    pass
