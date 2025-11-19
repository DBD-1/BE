from pydantic import BaseModel


class ClientGradeResponse(BaseModel):
    client_id: int
    average_score: float
    grade: str
    priority: int  # 1이 가장 높은 우선순위
