"""
Authentication Pydantic schemas for login and token management.
Defines data structures for authentication-related API endpoints.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserType, SocialProvider


class LoginRequest(BaseModel):
    """Schema for email/password login request."""
    email: EmailStr
    password: str
    remember_me: bool = False


class LoginResponse(BaseModel):
    """Schema for login response with tokens and user info."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # Seconds until access token expires
    user: dict  # User information


class TokenRefresh(BaseModel):
    """Schema for token refresh request."""
    refresh_token: str


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class SocialLoginResponse(BaseModel):
    """Schema for social login response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict
    is_new_user: bool = False  # True if this is first time login


class RegisterRequest(BaseModel):
    """Schema for user registration request."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=1, max_length=100)
    nickname: Optional[str] = Field(None, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    marketing_consent: bool = False
    terms_accepted: bool = Field(..., description="Must accept terms and conditions")

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
                "full_name": "김링크플레이스",
                "nickname": "linkuser",
                "phone_number": "010-1234-5678",
                "marketing_consent": True,
                "terms_accepted": True
            }
        }


class RegisterResponse(BaseModel):
    """Schema for registration response."""
    message: str
    user_id: int
    email: str
    verification_required: bool = True


class SocialLoginData(BaseModel):
    """Schema for social login user data from provider."""
    provider: SocialProvider
    social_id: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    nickname: Optional[str] = None
    profile_image_url: Optional[str] = None

    class Config:
        use_enum_values = True


class OAuth2CallbackRequest(BaseModel):
    """Schema for OAuth2 callback handling."""
    code: str
    state: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None


class LogoutRequest(BaseModel):
    """Schema for logout request."""
    refresh_token: Optional[str] = None
    logout_all_devices: bool = False


class VerifyTokenRequest(BaseModel):
    """Schema for token verification request."""
    token: str


class VerifyTokenResponse(BaseModel):
    """Schema for token verification response."""
    valid: bool
    user_id: Optional[int] = None
    email: Optional[str] = None
    expires_at: Optional[datetime] = None


class ChangeEmailRequest(BaseModel):
    """Schema for email change request."""
    new_email: EmailStr
    password: str


class ChangeEmailResponse(BaseModel):
    """Schema for email change response."""
    message: str
    verification_required: bool = True


class AccountActivation(BaseModel):
    """Schema for account activation."""
    token: str


class AccountDeactivation(BaseModel):
    """Schema for account deactivation request."""
    password: str
    reason: Optional[str] = None


class TwoFactorSetup(BaseModel):
    """Schema for 2FA setup request."""
    password: str


class TwoFactorSetupResponse(BaseModel):
    """Schema for 2FA setup response."""
    secret_key: str
    qr_code_url: str
    backup_codes: list[str]


class TwoFactorVerify(BaseModel):
    """Schema for 2FA verification."""
    code: str


class TwoFactorLogin(BaseModel):
    """Schema for 2FA login step."""
    email: EmailStr
    password: str
    totp_code: str
    remember_me: bool = False


class SessionInfo(BaseModel):
    """Schema for user session information."""
    session_id: str
    user_id: int
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime
    last_activity: datetime
    is_current: bool = False


class ActiveSessions(BaseModel):
    """Schema for user's active sessions."""
    sessions: list[SessionInfo]
    total: int


class RevokeSession(BaseModel):
    """Schema for session revocation."""
    session_id: str


class SecuritySettings(BaseModel):
    """Schema for user security settings."""
    two_factor_enabled: bool = False
    login_notifications: bool = True
    security_alerts: bool = True
    session_timeout: int = 3600  # seconds


class SecurityLog(BaseModel):
    """Schema for security log entry."""
    id: int
    user_id: int
    event_type: str  # 'login', 'logout', 'password_change', etc.
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = True
    details: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True


class SecurityLogs(BaseModel):
    """Schema for paginated security logs."""
    logs: list[SecurityLog]
    total: int
    page: int
    size: int


class AuthStats(BaseModel):
    """Schema for authentication statistics."""
    total_users: int
    active_users_today: int
    new_registrations_today: int
    social_login_percentage: float
    most_popular_provider: str
    failed_login_attempts_today: int
