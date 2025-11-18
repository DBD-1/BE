from fastapi import APIRouter, Query
from typing import List
from .schema import DeveloperWithSkill
from .service import search_developers_by_skill

router = APIRouter(prefix="/developers", tags=["Developers"])

@router.get(
    "/search",
    response_model=List[DeveloperWithSkill],
    summary="기술명으로 개발자 검색"
)
def search_developers(skill_name: str = Query(..., description="검색할 기술명")):
    return search_developers_by_skill(skill_name)
