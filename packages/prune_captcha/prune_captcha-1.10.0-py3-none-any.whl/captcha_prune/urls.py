from django.urls import path

from captcha_prune.views import create_captcha_view, verify_captcha_view

app_name = "captcha"

urlpatterns = [
    path("", create_captcha_view, name="create-captcha"),
    path("<str:uuid>/", verify_captcha_view, name="verify-captcha"),
]
