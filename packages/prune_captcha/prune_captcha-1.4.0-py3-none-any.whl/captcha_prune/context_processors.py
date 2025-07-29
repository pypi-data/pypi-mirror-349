from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def puzzle_static_path(request):
    try:
        path = settings.PUZZLE_IMAGE_STATIC_PATH
    except AttributeError:
        raise ImproperlyConfigured(
            "Vous devez définir PUZZLE_IMAGE_STATIC_PATH dans votre settings.py"
        )
    return {"PUZZLE_IMAGE_STATIC_PATH": path}
