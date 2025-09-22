"""
User model for authentication and user management.
Supports both regular users and merchants with social login integration.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class UserType(enum.Enum):
    """User type enumeration."""
    CUSTOMER = "customer"
    MERCHANT = "merchant"
    ADMIN = "admin"


class SocialProvider(enum.Enum):
    """Social login provider enumeration."""
    EMAIL = "email"
    NAVER = "naver"
    GOOGLE = "google"
    KAKAO = "kakao"


class User(Base):
    """
    User model for authentication and profile management.

    Supports multiple user types and social login providers.
    """
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Information
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    nickname = Column(String(50), unique=True, index=True, nullable=True)
    phone_number = Column(String(20), nullable=True)

    # Authentication
    hashed_password = Column(String(255), nullable=True)  # Nullable for social login
    user_type = Column(Enum(UserType), default=UserType.CUSTOMER, nullable=False)

    # Social Login Integration
    social_provider = Column(Enum(SocialProvider), default=SocialProvider.EMAIL, nullable=False)
    social_id = Column(String(100), nullable=True)  # ID from social provider
    profile_image_url = Column(Text, nullable=True)

    # Status and Permissions
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    # Profile Information
    bio = Column(Text, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(10), nullable=True)  # 'male', 'female', 'other'

    # Address Information
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)

    # Marketing and Preferences
    marketing_consent = Column(Boolean, default=False, nullable=False)
    push_notifications = Column(Boolean, default=True, nullable=False)
    email_notifications = Column(Boolean, default=True, nullable=False)

    # Points and Rewards
    total_points = Column(Integer, default=0, nullable=False)
    available_points = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    email_verified_at = Column(DateTime, nullable=True)

    # Relationships
    merchants = relationship("Merchant", back_populates="owner", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    point_transactions = relationship("PointTransaction", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', user_type='{self.user_type.value}')>"

    @property
    def is_merchant(self) -> bool:
        """Check if user is a merchant."""
        return self.user_type == UserType.MERCHANT

    @property
    def is_customer(self) -> bool:
        """Check if user is a customer."""
        return self.user_type == UserType.CUSTOMER

    @property
    def display_name(self) -> str:
        """Get display name (nickname or full name or email)."""
        return self.nickname or self.full_name or self.email

    @property
    def is_social_login(self) -> bool:
        """Check if user uses social login."""
        return self.social_provider != SocialProvider.EMAIL

    def add_points(self, amount: int) -> None:
        """Add points to user account."""
        self.total_points += amount
        self.available_points += amount

    def deduct_points(self, amount: int) -> bool:
        """
        Deduct points from user account.

        Returns:
            bool: True if successful, False if insufficient points
        """
        if self.available_points >= amount:
            self.available_points -= amount
            return True
        return False

    def update_last_login(self) -> None:
        """Update last login timestamp."""
        self.last_login_at = datetime.utcnow()

    def mark_email_verified(self) -> None:
        """Mark email as verified."""
        self.is_verified = True
        self.email_verified_at = datetime.utcnow()
