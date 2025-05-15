import os
from dotenv import load_dotenv

from helpers import get_env_list

load_dotenv()


# Application Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT")
SECRET_KEY = {
    "development": os.getenv("DEV_SECRET_KEY"),
    "staging": os.getenv("STAG_SECRET_KEY"),
    "production": os.getenv("PROD_SECRET_KEY"),
}.get(ENVIRONMENT, os.getenv("DEV_SECRET_KEY"))

# (External) API Key
BIGBOX_API_KEY = os.getenv("BIGBOX_API_KEY")
BIGBIX_API_URL = os.getenv("BIGBOX_API_URL")

# Database Configuration
DATABASES = {
    "development": {
        "ENGINE": os.getenv("DEV_DB_ENGINE"),
        "NAME": os.getenv("DEV_DB_NAME"),
        "USER": os.getenv("DEV_DB_USER"),
        "PASSWORD": os.getenv("DEV_DB_PASSWORD"),
        "HOST": os.getenv("DEV_DB_HOST"),
        "PORT": os.getenv("DEV_DB_PORT"),
    },
    "staging": {
        "ENGINE": os.getenv("STAG_DB_ENGINE"),
        "NAME": os.getenv("STAG_DB_NAME"),
        "USER": os.getenv("STAG_DB_USER"),
        "PASSWORD": os.getenv("STAG_DB_PASSWORD"),
        "HOST": os.getenv("STAG_DB_HOST"),
        "PORT": os.getenv("STAG_DB_PORT"),
    },
    "production": {
        "ENGINE": os.getenv("PROD_DB_ENGINE"),
        "NAME": os.getenv("PROD_DB_NAME"),
        "USER": os.getenv("PROD_DB_USER"),
        "PASSWORD": os.getenv("PROD_DB_PASSWORD"),
        "HOST": os.getenv("PROD_DB_HOST"),
        "PORT": os.getenv("PROD_DB_PORT"),
    },
}

# JWT Configuration
JWT_CONFIG = {
    "development": {
        "ACCESS_SECRET": os.getenv("DEV_JWT_ACCESS_SECRET"),
        "REFRESH_SECRET": os.getenv("DEV_JWT_REFRESH_SECRET"),
        "ACCESS_EXPIRES_IN": os.getenv("DEV_JWT_ACCESS_EXPIRES_IN"),
        "REFRESH_EXPIRES_IN": os.getenv("DEV_JWT_REFRESH_EXPIRES_IN"),
    },
    "staging": {
        "ACCESS_SECRET": os.getenv("STAG_JWT_ACCESS_SECRET"),
        "REFRESH_SECRET": os.getenv("STAG_JWT_REFRESH_SECRET"),
        "ACCESS_EXPIRES_IN": os.getenv("STAG_JWT_ACCESS_EXPIRES_IN"),
        "REFRESH_EXPIRES_IN": os.getenv("STAG_JWT_REFRESH_EXPIRES_IN"),
    },
    "production": {
        "ACCESS_SECRET": os.getenv("PROD_JWT_ACCESS_SECRET"),
        "REFRESH_SECRET": os.getenv("PROD_JWT_REFRESH_SECRET"),
        "ACCESS_EXPIRES_IN": os.getenv("PROD_JWT_ACCESS_EXPIRES_IN"),
        "REFRESH_EXPIRES_IN": os.getenv("PROD_JWT_REFRESH_EXPIRES_IN"),
    },
}

# CORS Configuration
CORS_CONFIG = {
    "development": {
        "ALLOWED_ORIGINS": get_env_list("DEV_CORS_ALLOWED_ORIGINS"),
        "ALLOWED_METHODS": get_env_list("DEV_CORS_ALLOWED_METHODS"),
        "ALLOWED_HEADERS": get_env_list("DEV_CORS_ALLOWED_HEADERS"),
        "EXPOSED_HEADERS": get_env_list("DEV_CORS_EXPOSED_HEADERS"),
    },
    "staging": {
        "ALLOWED_ORIGINS": get_env_list("STAG_CORS_ALLOWED_ORIGINS"),
        "ALLOWED_METHODS": get_env_list("STAG_CORS_ALLOWED_METHODS"),
        "ALLOWED_HEADERS": get_env_list("STAG_CORS_ALLOWED_HEADERS"),
        "EXPOSED_HEADERS": get_env_list("STAG_CORS_EXPOSED_HEADERS"),
    },
    "production": {
        "ALLOWED_ORIGINS": get_env_list("PROD_CORS_ALLOWED_ORIGINS"),
        "ALLOWED_METHODS": get_env_list("PROD_CORS_ALLOWED_METHODS"),
        "ALLOWED_HEADERS": get_env_list("PROD_CORS_ALLOWED_HEADERS"),
        "EXPOSED_HEADERS": get_env_list("PROD_CORS_EXPOSED_HEADERS"),
    },
}
