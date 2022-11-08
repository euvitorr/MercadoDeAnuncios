from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save


class CoreConfig(AppConfig):
    name = "core"
