"""
Main FastAPI application for LinkPlace backend.
Entry point for the LinkPlace platform API server.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.database import db_manager
from app import __version__

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting LinkPlace backend server...")
    try:
        await db_manager.startup()
        logger.info("Database connections established")
        logger.info(f"Server started successfully on environment: {settings.environment}")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down LinkPlace backend server...")
    try:
        await db_manager.shutdown()
        logger.info("Database connections closed")
        logger.info("Server shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application
    """
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="LinkPlace Platform Backend API",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan
    )

    # Add middleware
    setup_middleware(app)

    # Add exception handlers
    setup_exception_handlers(app)

    # Add routes
    setup_routes(app)

    return app


def setup_middleware(app: FastAPI) -> None:
    """
    Setup application middleware.

    Args:
        app: FastAPI application instance
    """
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )

    # Trusted host middleware (security)
    if not settings.debug:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["linkplace.co.kr", "*.linkplace.co.kr", "localhost"]
        )

    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log HTTP requests."""
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url}")

        # Process request
        response = await call_next(request)

        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} "
            f"({process_time:.3f}s) "
            f"{request.method} {request.url}"
        )

        return response


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Setup application exception handlers.

    Args:
        app: FastAPI application instance
    """
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions."""
        logger.warning(f"HTTP {exc.status_code}: {exc.detail} - {request.url}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "status_code": exc.status_code
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors."""
        logger.warning(f"Validation error: {exc} - {request.url}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": True,
                "message": "Request validation failed",
                "details": exc.errors(),
                "status_code": 422
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        logger.error(f"Unhandled exception: {exc} - {request.url}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": "Internal server error" if not settings.debug else str(exc),
                "status_code": 500
            }
        )


def setup_routes(app: FastAPI) -> None:
    """
    Setup application routes.

    Args:
        app: FastAPI application instance
    """

    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint."""
        return {
            "message": "Welcome to LinkPlace API",
            "version": __version__,
            "environment": settings.environment,
            "docs_url": "/docs" if settings.debug else None
        }

    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint."""
        try:
            # Check database connection
            from app.core.database import check_db_connection
            db_healthy = await check_db_connection()

            return {
                "status": "healthy" if db_healthy else "unhealthy",
                "version": __version__,
                "environment": settings.environment,
                "database": "connected" if db_healthy else "disconnected",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "status": "unhealthy",
                    "error": str(e) if settings.debug else "Service unavailable",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

    @app.get("/info", tags=["Info"])
    async def app_info():
        """Application information endpoint."""
        return {
            "name": settings.app_name,
            "version": __version__,
            "environment": settings.environment,
            "debug": settings.debug,
            "cors_origins": settings.cors_origins if settings.debug else None,
            "features": {
                "social_login": ["naver", "google", "kakao"],
                "authentication": "JWT",
                "database": "PostgreSQL",
                "cache": "Redis",
                "background_tasks": "Celery"
            }
        }

    # TODO: Add API routers here when endpoints are implemented
    # Example:
    # from app.api.v1.endpoints import auth, users
    # app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    # app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])


# Import required modules for the application
import time
from datetime import datetime


# Create the FastAPI application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
