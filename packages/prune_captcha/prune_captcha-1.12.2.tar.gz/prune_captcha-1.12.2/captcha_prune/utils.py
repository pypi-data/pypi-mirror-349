import os
import random

from django.conf import settings
from django.shortcuts import get_object_or_404

from captcha_prune.models import Captcha


def create_and_get_captcha() -> dict:
    captcha = Captcha.objects.create()

    _, _, puzzle_images_path = settings.PUZZLE_IMAGE_STATIC_PATH.rpartition("static/")
    puzzle_images = [
        f
        for f in os.listdir(settings.PUZZLE_IMAGE_STATIC_PATH)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))
    ]
    selected_image = random.choice(puzzle_images)

    return {
        "uuid": captcha.uuid,
        "width": captcha.width,
        "height": captcha.height,
        "piece_width": captcha.piece_width,
        "piece_height": captcha.piece_height,
        "pos_x_solution": captcha.pos_x_solution,
        "pos_y_solution": captcha.pos_y_solution,
        "piece_pos_x": captcha.piece_pos_x,
        "piece_pos_y": captcha.piece_pos_y,
        "image": f"{puzzle_images_path}{selected_image}",
    }


def verify_captcha(puzzle_uuid: str, pos_x_answer: int, pos_y_answer: int) -> bool:
    captcha = get_object_or_404(Captcha, uuid=puzzle_uuid)

    if (
        abs(captcha.pos_x_solution - pos_x_answer) <= captcha.precision
        and abs(captcha.pos_y_solution - pos_y_answer) <= captcha.precision
    ):
        return True
    else:
        return False
