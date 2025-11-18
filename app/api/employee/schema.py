from pydantic import BaseModel
from typing import Optional

class Employee(BaseModel):
    employee_id: int
    employee_name: Optional[str]
    rrn: Optional[str]
    education: Optional[str]
    years: Optional[int]
    job_type: str

    class Config:
        orm_mode = True
