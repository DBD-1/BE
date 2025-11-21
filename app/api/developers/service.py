from fastapi import HTTPException
from app.database import get_db_connection
import oracledb
from typing import List  

# 가용 개발자 검색 API 
def search_developers_by_skills(skill_names: List[str]):
    
    if not skill_names:
        return []

    bind_names = [f":s{i}" for i in range(len(skill_names))]
    bind_clause = ", ".join(bind_names)
    bind_params = {f"s{i}": name for i, name in enumerate(skill_names)}

    query = f"""
        SELECT 
            E.EMPLOYEE_ID,
            E.EMPLOYEE_NAME,
            D.SKILL_LEVEL,
            D.PROJECT_ASSIGNMENT_YN,
            LISTAGG(S.SKILL_NAME, ', ') WITHIN GROUP (ORDER BY S.SKILL_NAME) AS MATCHED_SKILLS
        FROM 
            EMPLOYEE E
            JOIN DEVELOPER D ON E.EMPLOYEE_ID = D.EMPLOYEE_ID
            JOIN EMPLOYEE_SKILL ES ON D.EMPLOYEE_ID = ES.EMPLOYEE_ID
            JOIN SKILL S ON ES.SKILL_ID = S.SKILL_ID
        WHERE 
            UPPER(S.SKILL_NAME) IN ({bind_clause})
        GROUP BY 
            E.EMPLOYEE_ID,
            E.EMPLOYEE_NAME,
            D.SKILL_LEVEL,
            D.PROJECT_ASSIGNMENT_YN
        ORDER BY 
            E.EMPLOYEE_ID
    """

    developers = []

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, bind_params)
                rows = cursor.fetchall()

                for row in rows:
                    skills_str = row[4]
                    skills_list = skills_str.split(", ") if skills_str else []

                    developers.append({
                        "employee_id": row[0],
                        "name": row[1],
                        "skill_level": row[2],
                        "project_assignment_yn": row[3],
                        "matched_skills": skills_list  # 결과: ["JAVA", "SPRING FRAMEWORK"]
                    })

                return developers

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")
    
# def search_developers_by_skill(skill_name: str):
    
#     query = """
#         SELECT 
#             E.EMPLOYEE_ID,
#             E.EMPLOYEE_NAME,
#             D.SKILL_LEVEL,
#             D.PROJECT_ASSIGNMENT_YN
#         FROM 
#             EMPLOYEE E
#             JOIN DEVELOPER D ON E.EMPLOYEE_ID = D.EMPLOYEE_ID
#             JOIN EMPLOYEE_SKILL ES ON D.EMPLOYEE_ID = ES.EMPLOYEE_ID
#             JOIN SKILL S ON ES.SKILL_ID = S.SKILL_ID
#         WHERE 
#             S.SKILL_NAME = :skill_name
#         ORDER BY 
#             E.EMPLOYEE_ID
#     """

#     developers = []

#     try:
#         with get_db_connection() as conn:
#             with conn.cursor() as cursor:
#                 cursor.execute(query, skill_name=skill_name)
#                 rows = cursor.fetchall()

#                 if not rows:
#                     raise HTTPException(status_code=404, detail="해당 기술을 가진 개발자 없음")

#                 for row in rows:
#                     developers.append({
#                         "employee_id": row[0],
#                         "name": row[1],
#                         "skill_level": row[2],
#                         "project_assignment_yn": row[3]
#                     })

#                 return developers

#     except oracledb.DatabaseError as e:
#         raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")



# 프로젝트 인력 투입 API ( 개발자 투입여부 0->1)
def assign_developer_by_click(employee_id: int):
    """
    개발자의 project_assignment_yn을 0 -> 1로 업데이트
    """
    update_query = """
        UPDATE DEVELOPER
        SET PROJECT_ASSIGNMENT_YN = 1
        WHERE EMPLOYEE_ID = :employee_id
          AND PROJECT_ASSIGNMENT_YN = 0
    """

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(update_query, employee_id=employee_id)
                if cursor.rowcount == 0:
                    # 이미 투입되었거나 존재하지 않음
                    raise HTTPException(status_code=404, detail="개발자가 없거나 이미 투입됨")
                conn.commit()
        return {"message": "개발자 투입 완료", "employee_id": employee_id}

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")