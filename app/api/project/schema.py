from pydantic import BaseModel
from typing import Optional
from datetime import date


class ProjectWithClientEvalStatus(BaseModel):
    project_id: int
    project_name: Optional[str]
    end_date: Optional[date]
    client_id: int
    client_name: Optional[str]
    eval_status: str  # "완료" 또는 "미완료"
