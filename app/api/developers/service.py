from fastapi import HTTPException
from app.database import get_db_connection
import oracledb

def search_developers_by_skill(skill_name: str):
    
    query = """
        SELECT 
            E.EMPLOYEE_ID,
            E.EMPLOYEE_NAME,
            D.SKILL_LEVEL,
            D.PROJECT_ASSIGNMENT_YN
        FROM 
            EMPLOYEE E
            JOIN DEVELOPER D ON E.EMPLOYEE_ID = D.EMPLOYEE_ID
            JOIN EMPLOYEE_SKILL ES ON D.EMPLOYEE_ID = ES.EMPLOYEE_ID
            JOIN SKILL S ON ES.SKILL_ID = S.SKILL_ID
        WHERE 
            S.SKILL_NAME = :skill_name
        ORDER BY 
            E.EMPLOYEE_ID
    """

    developers = []

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, skill_name=skill_name)
                rows = cursor.fetchall()

                if not rows:
                    raise HTTPException(status_code=404, detail="해당 기술을 가진 개발자 없음")

                for row in rows:
                    developers.append({
                        "employee_id": row[0],
                        "name": row[1],
                        "skill_level": row[2],
                        "project_assignment_yn": row[3]
                    })

                return developers

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")
