from typing import List
from fastapi import HTTPException
import oracledb

from app.database import get_db_connection
from app.api.project.schema import ProjectWithClientEvalStatus


def get_finished_projects_with_eval_status(employee_id: int) -> List[ProjectWithClientEvalStatus]:
    """
    직원이 참여한 종료된 프로젝트 + 고객평가 완료/미완료 상태 조회
    - 종료 프로젝트: PROJECT.END_DATE IS NOT NULL
    - 완료 여부: 해당 직원이 해당 CLIENT를 이미 평가한 적이 있는지 여부로 결정
    """
    query = """
        SELECT
            p.PROJECT_ID,
            p.PROJECT_NAME,
            p.END_DATE,
            c.CLIENT_ID,
            c.CLIENT_NAME,
            CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM CLIENT_EVALUATION ce
                    WHERE ce.CLIENT_ID = c.CLIENT_ID
                      AND ce.EVALUATOR_EMPLOYEE_ID = :employee_id
                )
                THEN '완료'
                ELSE '미완료'
            END AS EVAL_STATUS
        FROM PROJECT p
        JOIN PROJECT_ASSIGNMENT pa
          ON p.PROJECT_ID = pa.PROJECT_ID
        JOIN CLIENT c
          ON p.CLIENT_ID = c.CLIENT_ID
        WHERE pa.EMPLOYEE_ID = :employee_id
          AND p.END_DATE IS NOT NULL
        ORDER BY p.END_DATE DESC, p.PROJECT_ID
    """

    projects: List[ProjectWithClientEvalStatus] = []

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, employee_id=employee_id)
                rows = cursor.fetchall()

                for row in rows:
                    projects.append(
                        ProjectWithClientEvalStatus(
                            project_id=row[0],
                            project_name=row[1],
                            end_date=row[2],
                            client_id=row[3],
                            client_name=row[4],
                            eval_status=row[5],
                        )
                    )
    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")

    return projects
