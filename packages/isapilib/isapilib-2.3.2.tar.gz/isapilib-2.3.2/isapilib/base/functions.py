from django.conf import settings


def get_model_path(setting_name: str, default: str) -> str:
    return getattr(settings, setting_name, default)


def lazy_foreign_key(setting_name: str, default: str):
    return get_model_path(setting_name, default)
