from typing import List
from app.database import get_db_connection
from app.api.employee.schema import Employee
from fastapi import HTTPException
import oracledb

# 모든 개발자 직원 목록 조회(보유 기술 및 투입여부 포함)
def get_all_employees_service() -> List[Employee]:
    query = """
        SELECT 
            E.EMPLOYEE_ID, 
            E.EMPLOYEE_NAME, 
            E.JOB_TYPE,
            D.SKILL_LEVEL,
            D.PROJECT_ASSIGNMENT_YN,
            LISTAGG(S.SKILL_NAME, ', ') WITHIN GROUP (ORDER BY S.SKILL_NAME) AS SKILLS
        FROM 
            EMPLOYEE E
            JOIN DEVELOPER D ON E.EMPLOYEE_ID = D.EMPLOYEE_ID
            LEFT JOIN EMPLOYEE_SKILL ES ON E.EMPLOYEE_ID = ES.EMPLOYEE_ID
            LEFT JOIN SKILL S ON ES.SKILL_ID = S.SKILL_ID
        WHERE 
            E.JOB_TYPE = 'DEV'
        GROUP BY 
            E.EMPLOYEE_ID, 
            E.EMPLOYEE_NAME, 
            E.JOB_TYPE,
            D.SKILL_LEVEL,
            D.PROJECT_ASSIGNMENT_YN
        ORDER BY 
            E.EMPLOYEE_ID
    """

    employees = []

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                for row in rows:
                    # row 매핑
                    employee_id = row[0]
                    employee_name = row[1]
                    job_type = row[2]
                    skill_level = row[3]
                    project_assignment_yn = row[4]
                    skills_str = row[5]

                    skills_list = skills_str.split(", ") if skills_str else []

                    employees.append(Employee(
                        employee_id=employee_id,
                        employee_name=employee_name,
                        job_type=job_type,
                        skill_level=skill_level,
                        project_assignment_yn=project_assignment_yn,
                        skills=skills_list
                    ))

        return employees

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")

# def get_all_employees_service() -> List[Employee]:
#     query = """
#         SELECT EMPLOYEE_ID, EMPLOYEE_NAME, RRN, EDUCATION, YEARS, JOB_TYPE 
#         FROM EMPLOYEE
#         WHERE JOB_TYPE = 'DEV'
#     """

#     employees = []

#     try:
#         with get_db_connection() as conn:
#             with conn.cursor() as cursor:
#                 cursor.execute(query)
#                 rows = cursor.fetchall()

#                 for row in rows:
#                     employees.append(Employee(
#                         employee_id=row[0],
#                         employee_name=row[1],
#                         rrn=row[2],
#                         education=row[3],
#                         years=row[4],
#                         job_type=row[5]
#                     ))

#         return employees

#     except oracledb.DatabaseError as e:
#         raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")
