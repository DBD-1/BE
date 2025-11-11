from fastapi import FastAPI, Depends, HTTPException
from contextlib import contextmanager
import oracledb
from .database import init_db_pool, get_db_connection, close_db_pool
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db_pool()

@app.on_event("shutdown")
def shutdown_event():
    close_db_pool()

@contextmanager
def get_db_conn_manager():
    connection = None
    try:
        connection = get_db_connection()
        yield connection
    except Exception as e:
        # DB 연결 실패 시 500 에러 발생
        raise HTTPException(status_code=500, detail=f"DB connection error: {e}")
    finally:
        if connection:
            # 사용한 연결을 다시 풀(Pool)에 반환
            connection.close()
            

# 모든 직원 조회
class Employee(BaseModel):
    employee_id: int
    employee_name: Optional[str]  # NULL 허용 (Optional)
    rrn: Optional[str]
    education: Optional[str]
    years: Optional[int]
    job_type: str

@app.get(
    "/employees",
    response_model=List[Employee],
    summary="직원 목록 조회",              
    description="등록된 모든 직원의 정보를 조회합니다."  
)
def get_all_employees():
    """
    EMPLOYEE 테이블의 모든 직원 정보를 조회합니다.
    """
    query = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, RRN, EDUCATION, YEARS, JOB_TYPE FROM EMPLOYEE"
    
    employees = []
    with get_db_conn_manager() as conn:
        with conn.cursor() as cursor:
            try:
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
                # 쿼리 실행 중 오류가 발생하면 500 에러 반환
                raise HTTPException(status_code=500, detail=f"DB 쿼리 오류: {e}")