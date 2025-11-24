from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from .database import init_db_pool, close_db_pool

from app.api.developers.router import router as developer_router
from app.api.employee.router import router as employee_router
from app.api.skill.router import router as skill_router
from app.api.client.router import router as client_router
from app.api.client_evaluation.router import router as client_evaluation_router

from fastapi.middleware.cors import CORSMiddleware

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

# 2. CORS 설정 추가
origins = [
    # 개발 서버의 출처를 명시적으로 허용합니다.
    "http://localhost:8080", 
    # 프론트엔드 개발 시 자주 사용되는 다른 포트도 추가할 수 있습니다.
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # 허용할 출처 목록
    allow_credentials=True,         # 쿠키 등 자격 증명 허용 여부
    allow_methods=["*"],            # 모든 HTTP 메서드 (GET, POST, PATCH 등) 허용
    allow_headers=["*"],            # 모든 HTTP 헤더 허용
)

# 3. 라우터 등록
app.include_router(developer_router, prefix="/api")
app.include_router(employee_router, prefix="/api")
app.include_router(skill_router, prefix="/api")
app.include_router(client_router, prefix="/api")
app.include_router(client_evaluation_router, prefix="/api")