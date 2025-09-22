"""
Review model for user feedback and ratings.
Supports reviews for stores and campaigns with moderation capabilities.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class ReviewStatus(enum.Enum):
    """Review status enumeration."""
    PENDING = "pending"      # Awaiting moderation
    APPROVED = "approved"    # Approved and visible
    REJECTED = "rejected"    # Rejected by moderator
    FLAGGED = "flagged"      # Flagged for review
    HIDDEN = "hidden"        # Hidden by admin


class ReviewType(enum.Enum):
    """Review type enumeration."""
    STORE = "store"          # Review for a store
    CAMPAIGN = "campaign"    # Review for a campaign
    GENERAL = "general"      # General review


class Review(Base):
    """
    Review model for user feedback and ratings.

    Supports reviews for both stores and campaigns with comprehensive moderation.
    """
    __tablename__ = "reviews"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True, index=True)

    # Review Content
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    review_type = Column(Enum(ReviewType), default=ReviewType.STORE, nullable=False)

    # Status and Moderation
    status = Column(Enum(ReviewStatus), default=ReviewStatus.PENDING, nullable=False)
    is_verified_purchase = Column(Boolean, default=False, nullable=False)
    is_anonymous = Column(Boolean, default=False, nullable=False)

    # Rich Content
    images = Column(Text, nullable=True)  # JSON array of image URLs
    videos = Column(Text, nullable=True)  # JSON array of video URLs

    # Detailed Ratings (optional sub-ratings)
    service_rating = Column(Integer, nullable=True)     # 1-5
    quality_rating = Column(Integer, nullable=True)     # 1-5
    value_rating = Column(Integer, nullable=True)       # 1-5
    atmosphere_rating = Column(Integer, nullable=True)  # 1-5
    cleanliness_rating = Column(Integer, nullable=True) # 1-5

    # Visit Information
    visit_date = Column(DateTime, nullable=True)
    visit_purpose = Column(String(100), nullable=True)  # 'business', 'leisure', 'event', etc.
    party_size = Column(Integer, nullable=True)

    # Engagement and Social
    helpful_votes = Column(Integer, default=0, nullable=False)
    total_votes = Column(Integer, default=0, nullable=False)
    response_from_owner = Column(Text, nullable=True)
    response_date = Column(DateTime, nullable=True)

    # Tags and Categories
    tags = Column(Text, nullable=True)  # JSON array of tags
    sentiment_score = Column(Numeric(3, 2), nullable=True)  # -1 to 1

    # Moderation and Admin
    moderation_notes = Column(Text, nullable=True)
    flagged_reason = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    moderator_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # IP and Device Information
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    user_agent = Column(Text, nullable=True)
    device_type = Column(String(50), nullable=True)  # 'mobile', 'desktop', 'tablet'

    # Language and Localization
    language = Column(String(10), default="ko", nullable=False)
    translated_content = Column(Text, nullable=True)  # Auto-translated content

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    moderated_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="reviews")
    moderator = relationship("User", foreign_keys=[moderator_id])
    store = relationship("Store", back_populates="reviews")
    campaign = relationship("Campaign", back_populates="reviews")

    def __repr__(self) -> str:
        return f"<Review(id={self.id}, rating={self.rating}, status='{self.status.value}')>"

    @property
    def is_approved(self) -> bool:
        """Check if review is approved and visible."""
        return self.status == ReviewStatus.APPROVED

    @property
    def is_pending(self) -> bool:
        """Check if review is pending moderation."""
        return self.status == ReviewStatus.PENDING

    @property
    def helpfulness_percentage(self) -> float:
        """Calculate helpfulness percentage."""
        if self.total_votes == 0:
            return 0.0
        return (self.helpful_votes / self.total_votes) * 100

    @property
    def average_detailed_rating(self) -> float:
        """Calculate average of detailed ratings."""
        ratings = []
        if self.service_rating:
            ratings.append(self.service_rating)
        if self.quality_rating:
            ratings.append(self.quality_rating)
        if self.value_rating:
            ratings.append(self.value_rating)
        if self.atmosphere_rating:
            ratings.append(self.atmosphere_rating)
        if self.cleanliness_rating:
            ratings.append(self.cleanliness_rating)

        if not ratings:
            return float(self.rating)

        return sum(ratings) / len(ratings)

    @property
    def is_recent(self) -> bool:
        """Check if review was created in the last 30 days."""
        thirty_days_ago = datetime.utcnow().replace(day=datetime.utcnow().day - 30)
        return self.created_at >= thirty_days_ago

    @property
    def sentiment_label(self) -> str:
        """Get sentiment label based on sentiment score."""
        if self.sentiment_score is None:
            return "neutral"

        score = float(self.sentiment_score)
        if score >= 0.1:
            return "positive"
        elif score <= -0.1:
            return "negative"
        else:
            return "neutral"

    def approve(self, moderator_id: int = None) -> None:
        """Approve the review."""
        self.status = ReviewStatus.APPROVED
        self.moderated_at = datetime.utcnow()
        self.published_at = datetime.utcnow()
        if moderator_id:
            self.moderator_id = moderator_id

    def reject(self, reason: str = None, moderator_id: int = None) -> None:
        """Reject the review with optional reason."""
        self.status = ReviewStatus.REJECTED
        self.moderated_at = datetime.utcnow()
        if reason:
            self.rejection_reason = reason
        if moderator_id:
            self.moderator_id = moderator_id

    def flag(self, reason: str = None) -> None:
        """Flag the review for moderation."""
        self.status = ReviewStatus.FLAGGED
        if reason:
            self.flagged_reason = reason

    def hide(self, moderator_id: int = None) -> None:
        """Hide the review (admin action)."""
        self.status = ReviewStatus.HIDDEN
        self.moderated_at = datetime.utcnow()
        if moderator_id:
            self.moderator_id = moderator_id

    def add_helpful_vote(self) -> None:
        """Add a helpful vote."""
        self.helpful_votes += 1
        self.total_votes += 1

    def add_unhelpful_vote(self) -> None:
        """Add an unhelpful vote."""
        self.total_votes += 1

    def set_owner_response(self, response: str) -> None:
        """Set response from business owner."""
        self.response_from_owner = response
        self.response_date = datetime.utcnow()

    def update_sentiment(self, score: float) -> None:
        """Update sentiment score (-1 to 1)."""
        if -1 <= score <= 1:
            self.sentiment_score = score

    def can_be_edited_by_user(self, user_id: int) -> bool:
        """Check if review can be edited by the given user."""
        if self.user_id != user_id:
            return False

        # Allow editing within 24 hours of creation
        twenty_four_hours_ago = datetime.utcnow().replace(hour=datetime.utcnow().hour - 24)
        return self.created_at >= twenty_four_hours_ago

    def is_duplicate_content(self, content: str) -> bool:
        """Check if the provided content is duplicate."""
        return self.content.strip().lower() == content.strip().lower()

    @classmethod
    def get_average_rating_for_store(cls, store_id: int) -> float:
        """Get average rating for a specific store (class method for queries)."""
        # This would be implemented in the service layer with proper database queries
        pass

    @classmethod 
    def get_rating_distribution_for_store(cls, store_id: int) -> dict:
        """Get rating distribution (1-5 stars) for a store."""
        # This would be implemented in the service layer with proper database queries
        pass
