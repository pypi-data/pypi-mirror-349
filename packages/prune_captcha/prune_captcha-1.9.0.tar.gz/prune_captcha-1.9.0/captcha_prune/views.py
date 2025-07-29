from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from captcha_prune.models import Captcha
from captcha_prune.payloads import PuzzleAnswerPayload
from commons.decorators import use_payload


@require_POST
@csrf_exempt
def create_captcha_view(request: HttpRequest) -> HttpResponse:
    captcha = Captcha.objects.create()
    return JsonResponse(
        status=201,
        data={
            "uuid": str(captcha.uuid),
            "width": captcha.width,
            "height": captcha.height,
            "piece_width": captcha.piece_width,
            "piece_height": captcha.piece_height,
            "pos_x_solution": captcha.pos_x_solution,
            "pos_y_solution": captcha.pos_y_solution,
            "piece_pos_x": captcha.piece_pos_x,
            "piece_pos_y": captcha.piece_pos_y,
        },
    )


@require_GET
@use_payload(PuzzleAnswerPayload)
def verify_captcha_view(
    request: HttpRequest, uuid: str, payload: PuzzleAnswerPayload
) -> HttpResponse:
    captcha = get_object_or_404(Captcha, uuid=uuid)
    pos_x_answer = payload.pos_x_answer
    pos_y_answer = payload.pos_y_answer
    if (
        abs(captcha.pos_x_solution - pos_x_answer) <= captcha.precision
        and abs(captcha.pos_y_solution - pos_y_answer) <= captcha.precision
    ):
        return HttpResponse(status=304)
    else:
        return HttpResponse(status=401)
