from pydantic import BaseModel
from typing import Optional
from datetime import date

class Skill(BaseModel):
    skill_id: int
    skill_name: Optional[str]
