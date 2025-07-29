from pydantic import BaseModel


class PuzzleAnswerPayload(BaseModel):
    pos_x_answer: int
    pos_y_answer: int
