import os
import random

from django.conf import settings
from django.http import HttpRequest


def create_and_get_captcha(
    request, *, width=350, height=200, piece_width=80, piece_height=50, precision=2
) -> dict:
    pos_x_solution = random.randint(0, width - piece_width)
    pos_y_solution = random.randint(0, height - piece_height)
    piece_pos_x = random.randint(0, width - piece_width)
    piece_pos_y = random.randint(0, height - piece_height)
    _, _, puzzle_images_path = settings.PUZZLE_IMAGE_STATIC_PATH.rpartition("static/")
    puzzle_images = [
        f
        for f in os.listdir(settings.PUZZLE_IMAGE_STATIC_PATH)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))
    ]
    selected_image = random.choice(puzzle_images)
    request.session["pos_x_solution"] = pos_x_solution
    request.session["pos_y_solution"] = pos_y_solution
    request.session["precision"] = precision
    return {
        "width": width,
        "height": height,
        "piece_width": piece_width,
        "piece_height": piece_height,
        "pos_x_solution": pos_x_solution,
        "pos_y_solution": pos_y_solution,
        "piece_pos_x": piece_pos_x,
        "piece_pos_y": piece_pos_y,
        "image": f"{puzzle_images_path}{selected_image}",
    }


def verify_captcha(request: HttpRequest) -> bool:
    pos_x_answer = request.POST.get("pos_x_answer")
    pos_y_answer = request.POST.get("pos_Y_answer")
    if pos_x_answer is None or pos_y_answer is None:
        return False
    pos_x_solution = request.session.get("pos_x_solution")
    pos_y_solution = request.session.get("pos_y_solution")
    precision = request.session.get("precision")
    if (
        abs(pos_x_solution - pos_x_answer) <= precision
        and abs(pos_y_solution - pos_y_answer) <= precision
    ):
        return True
    else:
        return False
