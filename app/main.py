from fastapi import FastAPI, Depends, HTTPException, Query
from contextlib import contextmanager
import oracledb
from .database import init_db_pool, get_db_connection, close_db_pool
from pydantic import BaseModel
from typing import List, Optional
from app.api.developers.router import router as developer_router
from app.api.employee.router import router as employee_router
from app.api.skill.router import router as skill_router

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
            
# 라우터 등록
app.include_router(developer_router, prefix="/api")
app.include_router(employee_router, prefix="/api")
app.include_router(skill_router, prefix="/api")
