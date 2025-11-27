from fastapi import APIRouter, Query
from typing import List

from app.api.project.service import get_finished_projects_with_eval_status
from app.api.project.schema import ProjectWithClientEvalStatus
from .schema import (
    ClientEvalItem,
    ClientEvaluationSubmitRequest,
    ClientEvaluationSubmitResponse,
     ClientRanking,
)
from .service import (
    get_client_eval_items,
    submit_client_evaluation,
    get_client_ranking_list,
)

router = APIRouter(
    prefix="/client-evaluations",
    tags=["Client Evaluations"],
)


@router.get(
    "/projects",
    response_model=List[ProjectWithClientEvalStatus],
    summary="종료된 프로젝트 + 고객 평가 완료/미완료 조회",
)
def list_finished_projects_for_employee(
    employee_id: int = Query(..., description="로그인한 직원의 EMPLOYEE_ID"),
):
    """
    시나리오 2 - Step 2
    """
    return get_finished_projects_with_eval_status(employee_id)


@router.get(
    "/items",
    response_model=List[ClientEvalItem],
    summary="고객신용평가 항목 리스트 조회",
)
def list_client_eval_items():
    """
    시나리오 2 - Step 3
    """
    return get_client_eval_items()


@router.post(
    "",
    response_model=ClientEvaluationSubmitResponse,
    summary="고객 평가 저장",
)
def create_client_evaluation(payload: ClientEvaluationSubmitRequest):
    """
    시나리오 2 - Step 4~5
    """
    return submit_client_evaluation(payload)

@router.get(
    "/ranking",
    response_model=List[ClientRanking],
    summary="고객신용평가 점수 기준 고객 순위 조회",
)
def list_client_ranking():
    """
    시나리오 2 - (추가) 고객 우선순위/랭킹 페이지용 API

    - MV_CLIENT_AVG_SCORE 기준으로
      고객들의 평균 점수, 등급, 순위를 리턴
    """
    return get_client_ranking_list()