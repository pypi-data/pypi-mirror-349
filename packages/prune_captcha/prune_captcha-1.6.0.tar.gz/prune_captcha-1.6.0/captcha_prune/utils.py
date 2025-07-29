import os
import random
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.urls import reverse


def create_and_get_puzzle(request: HttpRequest) -> HttpResponse | dict:
    puzzle_path = getattr(settings, "PUZZLE_IMAGE_STATIC_PATH", None)
    try:
        response = requests.post(
            request.build_absolute_uri(reverse("captcha:create-captcha"))
        ).json()
    except requests.RequestException:
        return HttpResponse(status=502)
    request.session["puzzle_uuid"] = response["uuid"]
    puzzle_images = [
        f
        for f in os.listdir(puzzle_path)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))
    ]
    selected_image = random.choice(puzzle_images)
    return {
        "uuid": response["uuid"],
        "width": response["width"],
        "height": response["height"],
        "piece_width": response["piece_width"],
        "piece_height": response["piece_height"],
        "pos_x_solution": response["pos_x_solution"],
        "pos_y_solution": response["pos_y_solution"],
        "piece_pos_x": response["piece_pos_x"],
        "piece_pos_y": response["piece_pos_y"],
        "image": selected_image,
    }


def verify_captcha(
    request: HttpRequest,
    session_expired: HttpResponse,
    incorrect_captcha: HttpResponse,
    form,
) -> HttpResponse | None:
    puzzle_uuid = request.session.get("puzzle_uuid")
    if not puzzle_uuid:
        messages.error(request, "La session a expiré.")
        return session_expired
    try:
        base_url = request.build_absolute_uri(
            reverse("captcha:verify-captcha", kwargs={"uuid": puzzle_uuid}),
        )
        data = {
            "pos_x_answer": request.POST.get("pos_x_answer"),
            "pos_y_answer": request.POST.get("pos_y_answer"),
        }
        query_string = urlencode(data)
        full_url = f"{base_url}?{query_string}"
        response = requests.get(full_url)
        if response.status_code == 401:
            messages.error(request, "Captcha incorrect. Veuillez réessayer.")
            return incorrect_captcha
        del form.fields["pos_x_answer"]
        del form.fields["pos_y_answer"]
    except requests.RequestException:
        return HttpResponse(status=502)
