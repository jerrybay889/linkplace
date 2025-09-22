"""
LinkPlace Phase 1.5 Backend API
FastAPI 기반 백엔드 애플리케이션
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from contextlib import asynccontextmanager

from app.api.v1.endpoints import auth, stores, reviews, points, campaigns, archive
from app.middleware.middleware import log_requests

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작/종료 시 실행되는 함수"""
    logger.info("LinkPlace Phase 1.5 Backend API 시작")
    yield
    logger.info("LinkPlace Phase 1.5 Backend API 종료")


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="LinkPlace Phase 1.5 Backend API",
    description="매장 리뷰 및 포인트 시스템을 위한 백엔드 API",
    version="1.5.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경용, 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 커스텀 미들웨어 추가
app.middleware("http")(log_requests)

# API 라우터 등록
app.include_router(auth.router, prefix="/api/v1/auth", tags=["인증"])
app.include_router(stores.router, prefix="/api/v1/stores", tags=["매장"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["리뷰"])
app.include_router(points.router, prefix="/api/v1/points", tags=["포인트"])
app.include_router(campaigns.router, prefix="/api/v1/campaigns", tags=["캠페인"])
app.include_router(archive.router, prefix="/api/v1/archive", tags=["아카이브"])


@app.get("/", response_model=dict)
async def root():
    """루트 엔드포인트"""
    return {
        "message": "LinkPlace Phase 1.5 Backend API",
        "version": "1.5.0",
        "status": "running",
        "timestamp": int(time.time())
    }


@app.get("/health", response_model=dict)
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "timestamp": int(time.time()),
        "version": "1.5.0"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """전역 예외 처리기"""
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
