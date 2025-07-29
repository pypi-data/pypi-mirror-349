from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class DjangoPuzzleConfig(AppConfig):
    name = "django_puzzle"

    def ready(self):
        if not hasattr(settings, "PUZZLE_IMAGE_STATIC_PATH"):
            raise ImproperlyConfigured(
                "django-puzzle: vous devez définir PUZZLE_IMAGE_STATIC_PATH dans settings.py"
            )
