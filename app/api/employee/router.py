from fastapi import APIRouter
from typing import List
from .schema import Employee
from .service import get_all_employees_service

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.get(
    "",
    response_model=List[Employee],
    summary="모든 개발자 직원 목록 조회",
    description="등록된 모든 개발자 직원의 정보를 조회합니다."
)
def get_all_employees():
    return get_all_employees_service()
