"""
User Pydantic schemas for request/response validation.
Defines data structures for user-related API endpoints.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
from app.models.user import UserType, SocialProvider


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    full_name: Optional[str] = None
    nickname: Optional[str] = None
    phone_number: Optional[str] = None
    bio: Optional[str] = None
    user_type: UserType = UserType.CUSTOMER

    class Config:
        use_enum_values = True


class UserCreate(UserBase):
    """Schema for user creation."""
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    social_provider: SocialProvider = SocialProvider.EMAIL
    social_id: Optional[str] = None
    profile_image_url: Optional[str] = None
    marketing_consent: bool = False

    @validator("password")
    def validate_password(cls, v, values):
        """Validate password requirements."""
        if values.get("social_provider") == SocialProvider.EMAIL and not v:
            raise ValueError("Password is required for email registration")

        if v and len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        return v

    @validator("social_id")
    def validate_social_id(cls, v, values):
        """Validate social ID for social login."""
        social_provider = values.get("social_provider")
        if social_provider != SocialProvider.EMAIL and not v:
            raise ValueError("Social ID is required for social login")
        return v


class UserUpdate(BaseModel):
    """Schema for user profile updates."""
    full_name: Optional[str] = None
    nickname: Optional[str] = None
    phone_number: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = Field(None, regex="^(male|female|other)$")
    marketing_consent: Optional[bool] = None
    push_notifications: Optional[bool] = None
    email_notifications: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response data."""
    id: int
    is_active: bool
    is_verified: bool
    is_admin: bool
    total_points: int
    available_points: int
    created_at: datetime
    last_login_at: Optional[datetime]
    social_provider: SocialProvider
    profile_image_url: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class UserProfile(UserResponse):
    """Extended user profile schema with additional details."""
    postal_code: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    marketing_consent: bool
    push_notifications: bool
    email_notifications: bool
    email_verified_at: Optional[datetime] = None


class UserListResponse(BaseModel):
    """Schema for paginated user list."""
    users: List[UserResponse]
    total: int
    page: int
    size: int
    pages: int


class PasswordChange(BaseModel):
    """Schema for password change request."""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class PasswordReset(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class EmailVerification(BaseModel):
    """Schema for email verification."""
    token: str


class SocialLoginRequest(BaseModel):
    """Schema for social login request."""
    provider: SocialProvider
    access_token: str

    class Config:
        use_enum_values = True


class UserPointsResponse(BaseModel):
    """Schema for user points information."""
    user_id: int
    total_points: int
    available_points: int
    points_earned_today: int = 0
    points_expiring_soon: int = 0
    next_expiry_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserStatsResponse(BaseModel):
    """Schema for user statistics."""
    user_id: int
    total_reviews: int = 0
    total_campaigns_participated: int = 0
    average_rating_given: float = 0.0
    member_since: datetime
    last_activity: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserPreferences(BaseModel):
    """Schema for user notification preferences."""
    push_notifications: bool = True
    email_notifications: bool = True
    marketing_consent: bool = False
    sms_notifications: bool = False
    newsletter_subscription: bool = False


class UserSearch(BaseModel):
    """Schema for user search parameters."""
    query: Optional[str] = None
    user_type: Optional[UserType] = None
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None

    class Config:
        use_enum_values = True
