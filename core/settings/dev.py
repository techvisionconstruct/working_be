from .base import *
from config.constants import DATABASES, CORS_CONFIG

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += ["django_extensions"]

DATABASES = {
    "default": DATABASES["development"],
}
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS = CORS_CONFIG["development"]["ALLOWED_ORIGINS"]
# CORS_ALLOW_METHODS = CORS_CONFIG["development"]["ALLOWED_METHODS"]
# CORS_ALLOW_HEADERS = CORS_CONFIG["development"]["ALLOWED_HEADERS"]
# CORS_EXPOSE_HEADERS = CORS_CONFIG["development"]["EXPOSED_HEADERS"]
