import random
import uuid

from django.db import models

from commons.base_model import BaseModel


class Captcha(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    width = models.IntegerField(default=350)
    height = models.IntegerField(default=200)
    pos_x_solution = models.IntegerField(null=True, blank=True)
    pos_y_solution = models.IntegerField(null=True, blank=True)
    piece_pos_x = models.IntegerField(null=True, blank=True)
    piece_pos_y = models.IntegerField(null=True, blank=True)
    piece_width = models.IntegerField(default=80)
    piece_height = models.IntegerField(default=50)
    precision = models.IntegerField(default=2)

    def save(self, *args, **kwargs):
        if self.pos_x_solution is None:
            self.pos_x_solution = random.randint(0, self.width - self.piece_width)

        if self.pos_y_solution is None:
            self.pos_y_solution = random.randint(0, self.height - self.piece_height)

        if self.piece_pos_x is None:
            self.piece_pos_x = random.randint(0, self.width - self.piece_width)

        if self.piece_pos_y is None:
            self.piece_pos_y = random.randint(0, self.height - self.piece_height)

        super().save(*args, **kwargs)
