from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
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


try:
    from .local import *
except ImportError:
    pass
