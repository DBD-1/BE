from fastapi import APIRouter
from typing import List
from .schema import Skill
from .service import get_all_skill_service


# 기술 목록 조회 API 
router = APIRouter(
    prefix="/skill",
    tags=["skill"]
)


@router.get(
    "",
    response_model=List[Skill],
    summary="모든 기술 목록 조회",
    description="등록된 모든 기술의 정보를 조회합니다."
)
def get_all_employees():
    return get_all_skill_service()
