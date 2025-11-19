from fastapi import APIRouter
from .schema import ClientGradeResponse
from .service import get_client_grade_and_priority

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)


@router.get(
    "/{client_id}/grade",
    response_model=ClientGradeResponse,
    summary="고객 등급 및 우선순위 조회",
)
def read_client_grade(client_id: int):
    """
    새 프로젝트 생성 시, 해당 고객의 등급/우선순위를 알고 싶을 때 사용
    """
    return get_client_grade_and_priority(client_id)
