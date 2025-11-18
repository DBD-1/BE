from pydantic import BaseModel
from typing import Optional
from datetime import date

class DeveloperWithSkill(BaseModel):
    employee_id: int
    name: Optional[str]
    skill_level: Optional[str]
    project_assignment_yn: int

class DeveloperAssignUpdateResponse(BaseModel):
    message: str
    employee_id: int