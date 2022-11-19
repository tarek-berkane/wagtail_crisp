from .base import *
import environ

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-azrlvwwr3@%)31j*sc)z)vlj9s0a9&rqu7-0mqapb*5t#3fhqw"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = INSTALLED_APPS + [
    "django_browser_reload",
]

MIDDLEWARE = MIDDLEWARE + [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

INTERNAL_IPS = [
    "127.0.0.1",
]


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


try:
    from .local import *
except ImportError:
    pass
