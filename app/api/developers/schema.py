from pydantic import BaseModel
from typing import Optional

class DeveloperWithSkill(BaseModel):
    employee_id: int
    name: Optional[str]
    skill_level: Optional[str]
    project_assignment_yn: int
