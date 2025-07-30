import os
import random

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from captcha_prune.models import Captcha
from captcha_prune.payloads import PuzzleAnswerPayload
from commons.decorators import use_payload


@require_POST
@csrf_exempt
def create_captcha_view(request: HttpRequest) -> dict:
    captcha = Captcha.objects.create()
    request.session["puzzle_uuid"] = captcha.uuid

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


@require_GET
@use_payload(PuzzleAnswerPayload)
def verify_captcha_view(request: HttpRequest, payload: PuzzleAnswerPayload) -> bool:
    pos_x_answer = payload.pos_x_answer
    pos_y_answer = payload.pos_y_answer

    puzzle_uuid = request.session.get("puzzle_uuid")
    if not puzzle_uuid:
        messages.error(request, "La session a expiré.")
        return False
    captcha = get_object_or_404(Captcha, uuid=puzzle_uuid)

    if (
        abs(captcha.pos_x_solution - pos_x_answer) <= captcha.precision
        and abs(captcha.pos_y_solution - pos_y_answer) <= captcha.precision
    ):
        return True
    else:
        messages.error(request, "Captcha incorrect. Veuillez réessayer.")
        return False
