"""
미들웨어 모듈
"""

from fastapi import Request, Response
import time
import logging

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    """요청 로깅 미들웨어"""
    start_time = time.time()

    # 요청 정보 로그
    logger.info(f"Request: {request.method} {request.url}")

    try:
        # 다음 미들웨어 또는 엔드포인트 실행
        response = await call_next(request)

        # 응답 시간 계산
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        # 응답 정보 로그
        logger.info(f"Response: {response.status_code} - {process_time:.4f}s")

        return response

    except Exception as e:
        # 에러 로그
        process_time = time.time() - start_time
        logger.error(f"Error: {str(e)} - {process_time:.4f}s")
        raise


async def security_headers(request: Request, call_next):
    """보안 헤더 추가 미들웨어"""
    response = await call_next(request)

    # 보안 헤더 추가
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    return response
