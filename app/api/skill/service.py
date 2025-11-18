from typing import List
from app.database import get_db_connection
from app.api.skill.schema import Skill
from fastapi import HTTPException
import oracledb

def get_all_skill_service() -> List[Skill]:
    query = """
        SELECT SKILL_ID, SKILL_NAME
        FROM SKILL
    """

    skill = []

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                for row in rows:
                    skill.append(Skill(
                        skill_id=row[0],
                        skill_name=row[1],
                    ))

        return skill

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")
