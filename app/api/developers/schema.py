from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class DeveloperWithSkill(BaseModel):
    employee_id: int
    name: Optional[str]
    skill_level: Optional[str]
    project_assignment_yn: int
    matched_skills: Optional[List[str]] = [] # 입력한 기술 중 내가 보유한 기술 
    class Config:
        from_attributes = True 

class DeveloperAssignUpdateResponse(BaseModel):
    message: str
    employee_id: int