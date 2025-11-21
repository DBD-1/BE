from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from .database import init_db_pool, close_db_pool

from app.api.developers.router import router as developer_router
from app.api.employee.router import router as employee_router
from app.api.skill.router import router as skill_router
from app.api.client.router import router as client_router
from app.api.client_evaluation.router import router as client_evaluation_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # [시작 시] DB 연결
    print("🚀 Server Starting... Initializing DB Pool...")
    init_db_pool()
    yield
    # [종료 시] DB 연결 해제
    print("🛑 Server Shutting down... Closing DB Pool...")
    close_db_pool()

# 2. FastAPI 앱 생성 (lifespan 적용)
app = FastAPI(lifespan=lifespan)

# 3. 라우터 등록
app.include_router(developer_router, prefix="/api")
app.include_router(employee_router, prefix="/api")
app.include_router(skill_router, prefix="/api")
app.include_router(client_router, prefix="/api")
app.include_router(client_evaluation_router, prefix="/api")