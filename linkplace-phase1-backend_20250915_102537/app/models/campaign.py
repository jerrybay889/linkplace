"""
Campaign model for marketing campaigns.
Represents promotional campaigns created by merchants for their stores.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class CampaignStatus(enum.Enum):
    """Campaign status enumeration."""
    DRAFT = "draft"              # Created but not submitted
    PENDING = "pending"          # Submitted for approval
    APPROVED = "approved"        # Approved but not started
    ACTIVE = "active"           # Currently running
    PAUSED = "paused"           # Temporarily paused
    COMPLETED = "completed"      # Finished successfully
    CANCELLED = "cancelled"      # Cancelled before completion
    REJECTED = "rejected"        # Rejected by admin


class CampaignType(enum.Enum):
    """Campaign type enumeration."""
    DISCOUNT = "discount"        # Percentage or fixed amount discount
    CASHBACK = "cashback"        # Points or cash back reward
    BOGO = "bogo"               # Buy one get one offers
    FREE_ITEM = "free_item"     # Free item with purchase
    EVENT = "event"             # Special events or experiences
    LOYALTY = "loyalty"         # Loyalty program rewards
    REFERRAL = "referral"       # Referral bonuses
    SEASONAL = "seasonal"       # Seasonal promotions


class Campaign(Base):
    """
    Campaign model for promotional activities.

    Represents marketing campaigns that merchants create to attract customers.
    """
    __tablename__ = "campaigns"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False, index=True)

    # Basic Information
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    campaign_type = Column(Enum(CampaignType), nullable=False)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT, nullable=False)

    # Campaign Rules and Conditions
    terms_and_conditions = Column(Text, nullable=True)
    min_purchase_amount = Column(Numeric(10, 2), nullable=True)
    max_discount_amount = Column(Numeric(10, 2), nullable=True)
    discount_percentage = Column(Numeric(5, 2), nullable=True)  # 0-100%
    discount_amount = Column(Numeric(10, 2), nullable=True)     # Fixed amount

    # Reward and Points
    points_reward = Column(Integer, default=0, nullable=False)
    cashback_percentage = Column(Numeric(5, 2), nullable=True)
    cashback_amount = Column(Numeric(10, 2), nullable=True)

    # Campaign Limits
    total_budget = Column(Numeric(12, 2), nullable=False)
    remaining_budget = Column(Numeric(12, 2), nullable=False)
    max_participants = Column(Integer, nullable=True)
    max_uses_per_user = Column(Integer, default=1, nullable=False)
    max_daily_uses = Column(Integer, nullable=True)

    # Timing
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    # Targeting and Eligibility
    target_audience = Column(Text, nullable=True)  # JSON format for targeting criteria
    age_min = Column(Integer, nullable=True)
    age_max = Column(Integer, nullable=True)
    gender_target = Column(String(20), nullable=True)  # 'male', 'female', 'all'
    location_radius_km = Column(Numeric(6, 2), nullable=True)

    # Requirements
    requires_registration = Column(Boolean, default=True, nullable=False)
    requires_check_in = Column(Boolean, default=False, nullable=False)
    requires_review = Column(Boolean, default=False, nullable=False)
    requires_photo = Column(Boolean, default=False, nullable=False)
    requires_social_share = Column(Boolean, default=False, nullable=False)

    # Visual Content
    image_url = Column(Text, nullable=True)
    banner_image_url = Column(Text, nullable=True)
    gallery_images = Column(Text, nullable=True)  # JSON array

    # Social Media Integration
    hashtags = Column(Text, nullable=True)
    social_media_urls = Column(Text, nullable=True)  # JSON format

    # Performance Tracking
    total_views = Column(Integer, default=0, nullable=False)
    total_clicks = Column(Integer, default=0, nullable=False)
    total_participants = Column(Integer, default=0, nullable=False)
    total_completed = Column(Integer, default=0, nullable=False)
    total_spent = Column(Numeric(12, 2), default=0, nullable=False)

    # Engagement Metrics
    average_rating = Column(Numeric(3, 2), default=0, nullable=False)
    total_reviews = Column(Integer, default=0, nullable=False)
    total_shares = Column(Integer, default=0, nullable=False)
    conversion_rate = Column(Numeric(5, 2), default=0, nullable=False)

    # Settings and Preferences
    is_featured = Column(Boolean, default=False, nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)
    auto_approve_participants = Column(Boolean, default=True, nullable=False)
    send_notifications = Column(Boolean, default=True, nullable=False)

    # Admin and Moderation
    admin_notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    priority_score = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    approved_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    merchant = relationship("Merchant", back_populates="campaigns")
    store = relationship("Store", back_populates="campaigns")
    reviews = relationship("Review", back_populates="campaign", cascade="all, delete-orphan")
    point_transactions = relationship("PointTransaction", back_populates="campaign", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Campaign(id={self.id}, title='{self.title}', status='{self.status.value}')>"

    @property
    def is_active(self) -> bool:
        """Check if campaign is currently active."""
        now = datetime.utcnow()
        return (
            self.status == CampaignStatus.ACTIVE and
            self.start_date <= now <= self.end_date and
            self.remaining_budget > 0
        )

    @property
    def is_upcoming(self) -> bool:
        """Check if campaign is approved but not started yet."""
        return (
            self.status == CampaignStatus.APPROVED and
            datetime.utcnow() < self.start_date
        )

    @property
    def is_expired(self) -> bool:
        """Check if campaign has expired."""
        return datetime.utcnow() > self.end_date

    @property
    def budget_used(self) -> float:
        """Calculate how much budget has been used."""
        return float(self.total_budget - self.remaining_budget)

    @property
    def budget_usage_percentage(self) -> float:
        """Calculate budget usage as percentage."""
        if self.total_budget == 0:
            return 0.0
        return (self.budget_used / float(self.total_budget)) * 100

    @property
    def days_remaining(self) -> int:
        """Get number of days remaining in campaign."""
        if self.is_expired:
            return 0
        return (self.end_date - datetime.utcnow()).days

    @property
    def participation_rate(self) -> float:
        """Calculate participation rate based on views."""
        if self.total_views == 0:
            return 0.0
        return (self.total_participants / self.total_views) * 100

    def approve(self) -> None:
        """Approve the campaign."""
        self.status = CampaignStatus.APPROVED
        self.approved_at = datetime.utcnow()

    def reject(self, reason: str = None) -> None:
        """Reject the campaign with optional reason."""
        self.status = CampaignStatus.REJECTED
        if reason:
            self.rejection_reason = reason

    def start(self) -> None:
        """Start the campaign."""
        if self.status == CampaignStatus.APPROVED:
            self.status = CampaignStatus.ACTIVE
            self.started_at = datetime.utcnow()

    def pause(self) -> None:
        """Pause the campaign."""
        if self.status == CampaignStatus.ACTIVE:
            self.status = CampaignStatus.PAUSED

    def resume(self) -> None:
        """Resume a paused campaign."""
        if self.status == CampaignStatus.PAUSED:
            self.status = CampaignStatus.ACTIVE

    def complete(self) -> None:
        """Mark campaign as completed."""
        self.status = CampaignStatus.COMPLETED
        self.completed_at = datetime.utcnow()

    def cancel(self) -> None:
        """Cancel the campaign."""
        self.status = CampaignStatus.CANCELLED

    def can_participate(self, user_participation_count: int = 0) -> bool:
        """
        Check if a user can participate in this campaign.

        Args:
            user_participation_count: Number of times user has already participated

        Returns:
            bool: True if user can participate, False otherwise
        """
        if not self.is_active:
            return False

        if user_participation_count >= self.max_uses_per_user:
            return False

        if self.max_participants and self.total_participants >= self.max_participants:
            return False

        return True

    def deduct_budget(self, amount: float) -> bool:
        """
        Deduct amount from campaign budget.

        Args:
            amount: Amount to deduct

        Returns:
            bool: True if successful, False if insufficient budget
        """
        if self.remaining_budget >= amount:
            self.remaining_budget -= amount
            self.total_spent += amount
            return True
        return False

    def add_view(self) -> None:
        """Increment view count."""
        self.total_views += 1

    def add_click(self) -> None:
        """Increment click count."""
        self.total_clicks += 1

    def add_participant(self) -> None:
        """Increment participant count."""
        self.total_participants += 1
