"""
Application configuration using Pydantic Settings.
Manages environment variables and application settings.
"""
import os
from typing import List, Optional
from pydantic import BaseSettings, validator, Field


class Settings(BaseSettings):
    """Application settings with environment variable integration."""

    # Application Info
    app_name: str = Field(default="LinkPlace API", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="production", env="ENVIRONMENT")

    # Database Configuration
    database_url: str = Field(..., env="DATABASE_URL")
    database_url_sync: str = Field(..., env="DATABASE_URL_SYNC")

    # JWT Configuration
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    # OAuth2 Social Login - Naver
    naver_client_id: str = Field(..., env="NAVER_CLIENT_ID")
    naver_client_secret: str = Field(..., env="NAVER_CLIENT_SECRET") 
    naver_redirect_uri: str = Field(..., env="NAVER_REDIRECT_URI")

    # OAuth2 Social Login - Google
    google_client_id: str = Field(..., env="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(..., env="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = Field(..., env="GOOGLE_REDIRECT_URI")

    # OAuth2 Social Login - Kakao
    kakao_client_id: str = Field(..., env="KAKAO_CLIENT_ID")
    kakao_client_secret: str = Field(..., env="KAKAO_CLIENT_SECRET")
    kakao_redirect_uri: str = Field(..., env="KAKAO_REDIRECT_URI")

    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")

    # Celery Configuration
    celery_broker_url: str = Field(default="redis://localhost:6379/1", env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default="redis://localhost:6379/2", env="CELERY_RESULT_BACKEND")

    # CORS Configuration
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")

    # File Upload Configuration
    max_file_size: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB
    allowed_image_extensions: List[str] = Field(
        default=[".jpg", ".jpeg", ".png", ".gif", ".webp"], 
        env="ALLOWED_IMAGE_EXTENSIONS"
    )
    upload_dir: str = Field(default="uploads/", env="UPLOAD_DIR")

    # Email Configuration
    smtp_host: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_user: Optional[str] = Field(default=None, env="SMTP_USER")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    from_email: str = Field(default="noreply@linkplace.co.kr", env="FROM_EMAIL")

    @validator("cors_origins", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("allowed_image_extensions", pre=True)
    def assemble_allowed_extensions(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()
