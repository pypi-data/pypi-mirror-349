import uuid

from django.test import TestCase
from django.urls import reverse

from captcha_prune.models import Captcha


class CreateCaptchaViewTestCase(TestCase):
    def test_create_captcha_with_GET_method(self):
        response = self.client.get(reverse("create-captcha"))
        self.assertEqual(response.status_code, 405)

    def test_create_captcha_with_POST_method(self):
        response = self.client.post(reverse("create-captcha"))
        self.assertEqual(response.status_code, 201)

        data = response.json()
        captcha = Captcha.objects.get(uuid=data["uuid"])
        self.assertIsNotNone(captcha)


class VerifyCaptchaViewTestCase(TestCase):
    def setUp(self):
        self.captcha = Captcha.objects.create()
        self.pos_x_solution = self.captcha.pos_x_solution
        self.pos_y_solution = self.captcha.pos_y_solution

    def test_verify_captcha_with_POST_method(self):
        response = self.client.post(
            reverse("verify-captcha", kwargs={"uuid": str(uuid.uuid4())}),
            data={
                "pos_x_answer": self.pos_x_solution,
                "pos_y_answer": self.pos_y_solution,
            },
        )
        self.assertEqual(response.status_code, 405)

    def test_verify_captcha_with_bad_uuid(self):
        response = self.client.get(
            reverse("verify-captcha", kwargs={"uuid": str(uuid.uuid4())}),
            data={
                "pos_x_answer": self.pos_x_solution,
                "pos_y_answer": self.pos_y_solution,
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_verify_captcha_with_good_uuid_but_bad_answer(self):
        response = self.client.get(
            reverse("verify-captcha", kwargs={"uuid": str(self.captcha.uuid)}),
            data={
                "pos_x_answer": self.pos_x_solution - 20,
                "pos_y_answer": self.pos_y_solution - 20,
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_verify_captcha_with_good_uuid_and_good_answer(self):
        response = self.client.get(
            reverse("verify-captcha", kwargs={"uuid": str(self.captcha.uuid)}),
            data={
                "pos_x_answer": self.pos_x_solution,
                "pos_y_answer": self.pos_y_solution,
            },
        )
        self.assertEqual(response.status_code, 304)
