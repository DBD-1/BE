from fastapi import APIRouter, Query, HTTPException
from typing import List
from .schema import DeveloperWithSkill, DeveloperAssignUpdateResponse
from .service import search_developers_by_skills, assign_developer_by_click


# 가용 개발자 검색 API 
router = APIRouter(prefix="/developers", tags=["Developers"])

@router.get(
    "/search",
    response_model=List[DeveloperWithSkill],
    summary="기술명으로 개발자 검색"
)
def search_developers(
    skill_names: List[str] = Query(..., description="검색할 기술명 리스트 (예: Java, Python)")
):
    return search_developers_by_skills(skill_names)


# 프로젝트 인력 투입 API
@router.patch(
    "/{employee_id}/assign",
    response_model=DeveloperAssignUpdateResponse,
    summary="개발자 투입 상태 변경 (0 -> 1)"
)
def assign_developer(employee_id: int):
    return assign_developer_by_click(employee_id)


