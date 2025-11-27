from typing import List, Tuple
from fastapi import HTTPException
import oracledb

from app.database import get_db_connection
from app.api.client_evaluation.schema import (
    ClientEvalItem,
    ClientEvaluationSubmitRequest,
    ClientEvaluationSubmitResponse,
    ClientRanking,
)


# 1) 고객신용평가 항목 리스트 조회
def get_client_eval_items() -> List[ClientEvalItem]:
    query = """
        SELECT CLIENT_ITEM_CODE, ITEM_NAME
        FROM CLIENT_EVAL_ITEM
        ORDER BY CLIENT_ITEM_CODE
    """

    items: List[ClientEvalItem] = []

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    items.append(
                        ClientEvalItem(
                            client_item_code=row[0],
                            item_name=row[1],
                        )
                    )
    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")

    return items


# 2) 특정 고객의 평균 점수 & 등급 계산 (재사용 가능 함수)
def calculate_client_avg_and_grade(client_id: int) -> Tuple[float, str]:
    """
    CLIENT_EVALUATION_SCORE + CLIENT_EVALUATION 을 조인해서
    해당 CLIENT 의 전체 평가 점수 평균과 등급을 계산
    """
    avg_query = """
        SELECT AVG(s.SCORE)
        FROM CLIENT_EVALUATION_SCORE s
        JOIN CLIENT_EVALUATION e
          ON s.CLIENT_EVALUATION_ID = e.CLIENT_EVALUATION_ID
        WHERE e.CLIENT_ID = :client_id
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(avg_query, client_id=client_id)
                row = cursor.fetchone()
                if not row or row[0] is None:
                    # 평가가 하나도 없는 경우
                    return 0.0, "D"

                avg_score = float(row[0])

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")

    # 등급 규칙
    if avg_score >= 90:
        grade = "A"
    elif avg_score >= 80:
        grade = "B"
    elif avg_score >= 70:
        grade = "C"
    else:
        grade = "D"

    return avg_score, grade


# 3) 고객 평가 제출
def submit_client_evaluation(
    payload: ClientEvaluationSubmitRequest,
) -> ClientEvaluationSubmitResponse:
    # 점수 범위 간단 검증
    for s in payload.scores:
        if s.score < 0 or s.score > 100:
            raise HTTPException(status_code=400, detail="점수는 0~100 사이여야 합니다.")

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # 1) CLIENT_EVALUATION_ID 생성
                cursor.execute("SELECT SQ_CLIENT_EVALUATION_ID.NEXTVAL FROM DUAL")
                client_eval_id = cursor.fetchone()[0]

                # 2) CLIENT_EVALUATION INSERT
                insert_eval_sql = """
                    INSERT INTO CLIENT_EVALUATION (
                        CLIENT_EVALUATION_ID,
                        CLIENT_ID,
                        EVALUATOR_EMPLOYEE_ID,
                        EVAL_DATE
                    ) VALUES (
                        :client_eval_id,
                        :client_id,
                        :evaluator_employee_id,
                        SYSDATE
                    )
                """
                cursor.execute(
                    insert_eval_sql,
                    client_eval_id=client_eval_id,
                    client_id=payload.client_id,
                    evaluator_employee_id=payload.evaluator_employee_id,
                )

                # 3) CLIENT_EVALUATION_SCORE 여러 행 INSERT
                insert_score_sql = """
                    INSERT INTO CLIENT_EVALUATION_SCORE (
                        CLIENT_EVALUATION_ID,
                        CLIENT_ITEM_CODE,
                        SCORE
                    ) VALUES (
                        :client_eval_id,
                        :client_item_code,
                        :score
                    )
                """
                for score_item in payload.scores:
                    cursor.execute(
                        insert_score_sql,
                        client_eval_id=client_eval_id,
                        client_item_code=score_item.client_item_code,
                        score=score_item.score,
                    )

                # 커밋
                conn.commit()

        # 4) 새 평가까지 포함한 평균/등급 다시 계산
        avg_score, grade = calculate_client_avg_and_grade(payload.client_id)

        return ClientEvaluationSubmitResponse(
            message="고객 평가가 저장되었습니다.",
            client_evaluation_id=client_eval_id,
            client_id=payload.client_id,
            average_score=avg_score,
            grade=grade,
        )

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")

# 4) 고객신용평가 점수 기준 고객 순위 조회
def get_client_ranking_list() -> List[ClientRanking]:
    """
    MV_CLIENT_AVG_SCORE + CLIENT 를 이용해서
    고객들의 평균 점수/등급/순위를 한 번에 조회.

    - 평균점수 내림차순
    - 동점일 경우 같은 rank (DENSE_RANK)
    """
    query = """
        SELECT
            c.CLIENT_ID,
            c.CLIENT_NAME,
            m.AVG_SCORE,
            CASE
                WHEN m.AVG_SCORE >= 90 THEN 'A'
                WHEN m.AVG_SCORE >= 80 THEN 'B'
                WHEN m.AVG_SCORE >= 70 THEN 'C'
                ELSE 'D'
            END AS GRADE,
            DENSE_RANK() OVER (ORDER BY m.AVG_SCORE DESC, c.CLIENT_ID) AS RANK_NO
        FROM MV_CLIENT_AVG_SCORE m
        JOIN CLIENT c
          ON c.CLIENT_ID = m.CLIENT_ID
        ORDER BY RANK_NO, c.CLIENT_ID
    """

    rankings: List[ClientRanking] = []

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                for row in rows:
                    rankings.append(
                        ClientRanking(
                            client_id=row[0],
                            client_name=row[1],
                            average_score=float(row[2]),
                            grade=row[3],
                            rank=int(row[4]),
                        )
                    )

    except oracledb.DatabaseError as e:
        # MV가 없거나, 컬럼명이 다른 경우도 여기로 떨어질 수 있음
        raise HTTPException(status_code=500, detail=f"고객 순위 조회 중 DB 오류: {e}")

    return rankings