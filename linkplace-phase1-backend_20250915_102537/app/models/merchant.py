"""
Merchant model for business management.
Represents merchants who can create stores and manage campaigns.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class MerchantStatus(enum.Enum):
    """Merchant status enumeration."""
    PENDING = "pending"      # Application submitted, waiting for approval
    APPROVED = "approved"    # Approved and active
    SUSPENDED = "suspended"  # Temporarily suspended
    REJECTED = "rejected"    # Application rejected
    INACTIVE = "inactive"    # Voluntarily inactive


class BusinessType(enum.Enum):
    """Business type enumeration."""
    RESTAURANT = "restaurant"
    CAFE = "cafe"
    RETAIL = "retail"
    SERVICE = "service"
    BEAUTY = "beauty"
    FITNESS = "fitness"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    HEALTHCARE = "healthcare"
    OTHER = "other"


class Merchant(Base):
    """
    Merchant model for business management.

    Represents businesses that can create stores and manage campaigns.
    """
    __tablename__ = "merchants"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Business Information
    business_name = Column(String(200), nullable=False, index=True)
    business_registration_number = Column(String(50), unique=True, nullable=False)
    business_type = Column(Enum(BusinessType), nullable=False)
    description = Column(Text, nullable=True)

    # Contact Information
    contact_person = Column(String(100), nullable=False)
    contact_phone = Column(String(20), nullable=False)
    contact_email = Column(String(255), nullable=False)

    # Address Information
    business_address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default="South Korea", nullable=False)

    # Status and Verification
    status = Column(Enum(MerchantStatus), default=MerchantStatus.PENDING, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_documents = Column(Text, nullable=True)  # JSON or comma-separated file URLs

    # Business Details
    website_url = Column(String(500), nullable=True)
    social_media_urls = Column(Text, nullable=True)  # JSON format
    logo_url = Column(Text, nullable=True)
    business_hours = Column(Text, nullable=True)  # JSON format

    # Financial Information
    bank_account_number = Column(String(50), nullable=True)
    bank_name = Column(String(100), nullable=True)
    account_holder_name = Column(String(100), nullable=True)
    tax_id = Column(String(50), nullable=True)

    # Settings and Preferences
    commission_rate = Column(Numeric(5, 4), default=0.03, nullable=False)  # 3% default
    auto_approve_campaigns = Column(Boolean, default=False, nullable=False)
    max_campaign_budget = Column(Numeric(12, 2), nullable=True)
    notification_preferences = Column(Text, nullable=True)  # JSON format

    # Statistics
    total_stores = Column(Integer, default=0, nullable=False)
    active_campaigns = Column(Integer, default=0, nullable=False)
    total_revenue = Column(Numeric(12, 2), default=0, nullable=False)
    rating = Column(Numeric(3, 2), default=0, nullable=False)
    total_reviews = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    approved_at = Column(DateTime, nullable=True)
    last_activity_at = Column(DateTime, nullable=True)

    # Relationships
    owner = relationship("User", back_populates="merchants")
    stores = relationship("Store", back_populates="merchant", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="merchant", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Merchant(id={self.id}, business_name='{self.business_name}', status='{self.status.value}')>"

    @property
    def is_active(self) -> bool:
        """Check if merchant is active and approved."""
        return self.status == MerchantStatus.APPROVED and self.is_verified

    @property
    def display_name(self) -> str:
        """Get display name for the merchant."""
        return self.business_name

    @property
    def average_rating(self) -> float:
        """Get average rating as float."""
        return float(self.rating) if self.rating else 0.0

    def approve(self) -> None:
        """Approve the merchant."""
        self.status = MerchantStatus.APPROVED
        self.is_verified = True
        self.approved_at = datetime.utcnow()

    def suspend(self) -> None:
        """Suspend the merchant."""
        self.status = MerchantStatus.SUSPENDED

    def reject(self) -> None:
        """Reject the merchant application."""
        self.status = MerchantStatus.REJECTED

    def reactivate(self) -> None:
        """Reactivate a suspended merchant."""
        if self.status == MerchantStatus.SUSPENDED:
            self.status = MerchantStatus.APPROVED

    def update_stats(self) -> None:
        """Update merchant statistics (should be called periodically)."""
        # This would typically be implemented to calculate from related records
        pass

    def can_create_campaign(self, budget_amount: float) -> bool:
        """
        Check if merchant can create a campaign with the given budget.

        Args:
            budget_amount: Proposed campaign budget

        Returns:
            bool: True if can create campaign, False otherwise
        """
        if not self.is_active:
            return False

        if self.max_campaign_budget and budget_amount > float(self.max_campaign_budget):
            return False

        return True

    def update_last_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity_at = datetime.utcnow()
