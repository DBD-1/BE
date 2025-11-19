from fastapi import HTTPException

from .schema import ClientGradeResponse
from app.api.client_evaluation.service import calculate_client_avg_and_grade


def get_client_grade_and_priority(client_id: int) -> ClientGradeResponse:
    try:
        avg_score, grade = calculate_client_avg_and_grade(client_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"평가 조회 오류: {e}")

    # 등급 → 우선순위 매핑
    priority_map = {
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4,
    }
    priority = priority_map.get(grade, 4)

    return ClientGradeResponse(
        client_id=client_id,
        average_score=avg_score,
        grade=grade,
        priority=priority,
    )
