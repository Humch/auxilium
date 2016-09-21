from django.apps import AppConfig


class GedConfig(AppConfig):
    name = 'ged'

    def ready(self):
        import ged.signals