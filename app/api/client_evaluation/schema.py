from pydantic import BaseModel
from typing import List


class ClientEvalItem(BaseModel):
    client_item_code: int
    item_name: str


class ClientEvalScoreInput(BaseModel):
    client_item_code: int
    score: int  # 0 ~ 100


class ClientEvaluationSubmitRequest(BaseModel):
    evaluator_employee_id: int
    project_id: int      # 프론트에서 선택한 프로젝트
    client_id: int       # 프로젝트에서 얻은 CLIENT_ID
    scores: List[ClientEvalScoreInput]


class ClientEvaluationSubmitResponse(BaseModel):
    message: str
    client_evaluation_id: int
    client_id: int
    average_score: float
    grade: str
