from typing import List
from app.database import get_db_connection
from app.api.employee.schema import Employee
from fastapi import HTTPException
import oracledb

def get_all_employees_service() -> List[Employee]:
    query = """
        SELECT EMPLOYEE_ID, EMPLOYEE_NAME, RRN, EDUCATION, YEARS, JOB_TYPE 
        FROM EMPLOYEE
    """

    employees = []

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                for row in rows:
                    employees.append(Employee(
                        employee_id=row[0],
                        employee_name=row[1],
                        rrn=row[2],
                        education=row[3],
                        years=row[4],
                        job_type=row[5]
                    ))

        return employees

    except oracledb.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")
