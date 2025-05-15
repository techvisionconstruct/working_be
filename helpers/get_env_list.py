import os


def get_env_list(var_name, default=""):
    value = os.getenv(var_name, default)
    return [item.strip() for item in value.split(",") if item.strip()]
