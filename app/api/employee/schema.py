from pydantic import BaseModel
from typing import Optional, List

class Employee(BaseModel):
    employee_id: int
    employee_name: Optional[str]
    job_type: str
    skill_level: Optional[str]
    project_assignment_yn: int
    skills: List[str] = [] #개발자의 전체 보유기술

    class Config:
        orm_mode = True
