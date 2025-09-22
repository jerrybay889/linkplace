"""
Point transaction model for reward system.
Tracks all point-related transactions including earning and spending.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class TransactionType(enum.Enum):
    """Point transaction type enumeration."""
    EARNED = "earned"        # Points earned by user
    SPENT = "spent"          # Points spent by user
    REFUNDED = "refunded"    # Points refunded to user
    EXPIRED = "expired"      # Points expired
    ADJUSTED = "adjusted"    # Administrative adjustment
    BONUS = "bonus"          # Bonus points awarded
    PENALTY = "penalty"      # Points deducted as penalty


class TransactionSource(enum.Enum):
    """Source of the transaction."""
    CAMPAIGN = "campaign"              # From campaign participation
    REVIEW = "review"                  # From writing reviews
    REFERRAL = "referral"              # From referrals
    PURCHASE = "purchase"              # From purchases
    SIGNUP = "signup"                  # From account registration
    DAILY_CHECKIN = "daily_checkin"    # From daily check-in
    EVENT = "event"                    # From special events
    ADMIN = "admin"                    # Administrative action
    SOCIAL_SHARE = "social_share"      # From social media sharing
    BIRTHDAY = "birthday"              # Birthday bonus
    EXPIRATION = "expiration"          # Point expiration
    OTHER = "other"                    # Other sources


class TransactionStatus(enum.Enum):
    """Transaction status enumeration."""
    PENDING = "pending"      # Transaction is pending
    COMPLETED = "completed"  # Transaction completed successfully
    FAILED = "failed"        # Transaction failed
    CANCELLED = "cancelled"  # Transaction was cancelled
    REVERSED = "reversed"    # Transaction was reversed


class PointTransaction(Base):
    """
    Point transaction model for reward system.

    Tracks all point earning, spending, and management activities.
    """
    __tablename__ = "point_transactions"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True, index=True)

    # Transaction Details
    transaction_type = Column(Enum(TransactionType), nullable=False, index=True)
    source = Column(Enum(TransactionSource), nullable=False, index=True)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.COMPLETED, nullable=False)

    # Point Information
    points = Column(Integer, nullable=False)  # Positive for earned, negative for spent
    balance_before = Column(Integer, nullable=False)
    balance_after = Column(Integer, nullable=False)

    # Transaction Context
    description = Column(Text, nullable=False)
    reference_id = Column(String(100), nullable=True, index=True)  # External reference
    reference_type = Column(String(50), nullable=True)  # Type of reference

    # Expiration Information (for earned points)
    expires_at = Column(DateTime, nullable=True)
    is_expired = Column(Boolean, default=False, nullable=False)

    # Related Transaction (for refunds/reversals)
    related_transaction_id = Column(Integer, ForeignKey("point_transactions.id"), nullable=True)

    # Metadata
    metadata = Column(Text, nullable=True)  # JSON for additional data
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)

    # Administrative
    admin_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    admin_notes = Column(Text, nullable=True)

    # Processing Information
    processed_at = Column(DateTime, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="point_transactions")
    campaign = relationship("Campaign", back_populates="point_transactions")
    admin_user = relationship("User", foreign_keys=[admin_user_id])
    related_transaction = relationship("PointTransaction", remote_side=[id])

    def __repr__(self) -> str:
        return f"<PointTransaction(id={self.id}, user_id={self.user_id}, points={self.points}, type='{self.transaction_type.value}')>"

    @property
    def is_earning_transaction(self) -> bool:
        """Check if this is a point earning transaction."""
        return self.transaction_type in [
            TransactionType.EARNED, 
            TransactionType.REFUNDED, 
            TransactionType.BONUS
        ]

    @property
    def is_spending_transaction(self) -> bool:
        """Check if this is a point spending transaction."""
        return self.transaction_type in [
            TransactionType.SPENT,
            TransactionType.EXPIRED,
            TransactionType.PENALTY
        ]

    @property
    def is_completed(self) -> bool:
        """Check if transaction is completed."""
        return self.status == TransactionStatus.COMPLETED

    @property
    def is_pending(self) -> bool:
        """Check if transaction is pending."""
        return self.status == TransactionStatus.PENDING

    @property
    def absolute_points(self) -> int:
        """Get absolute value of points (always positive)."""
        return abs(self.points)

    @property
    def is_expiring_soon(self) -> bool:
        """Check if points are expiring within 30 days."""
        if not self.expires_at or self.is_expired:
            return False

        thirty_days_from_now = datetime.utcnow().replace(day=datetime.utcnow().day + 30)
        return self.expires_at <= thirty_days_from_now

    @property
    def days_until_expiry(self) -> int:
        """Get number of days until expiry."""
        if not self.expires_at or self.is_expired:
            return 0

        delta = self.expires_at - datetime.utcnow()
        return max(0, delta.days)

    def complete(self) -> None:
        """Mark transaction as completed."""
        self.status = TransactionStatus.COMPLETED
        self.processed_at = datetime.utcnow()

    def fail(self, reason: str = None) -> None:
        """Mark transaction as failed."""
        self.status = TransactionStatus.FAILED
        self.processed_at = datetime.utcnow()
        if reason:
            self.admin_notes = reason

    def cancel(self, reason: str = None) -> None:
        """Cancel the transaction."""
        self.status = TransactionStatus.CANCELLED
        self.processed_at = datetime.utcnow()
        if reason:
            self.admin_notes = reason

    def reverse(self, admin_user_id: int, reason: str = None) -> 'PointTransaction':
        """
        Create a reverse transaction.

        Args:
            admin_user_id: ID of admin performing the reversal
            reason: Reason for reversal

        Returns:
            PointTransaction: New reverse transaction
        """
        reverse_transaction = PointTransaction(
            user_id=self.user_id,
            transaction_type=TransactionType.ADJUSTED,
            source=TransactionSource.ADMIN,
            status=TransactionStatus.COMPLETED,
            points=-self.points,  # Opposite amount
            balance_before=0,  # Will be set by service
            balance_after=0,   # Will be set by service
            description=f"Reversal of transaction #{self.id}: {reason or 'Administrative reversal'}",
            related_transaction_id=self.id,
            admin_user_id=admin_user_id,
            admin_notes=reason,
            processed_at=datetime.utcnow()
        )

        self.status = TransactionStatus.REVERSED
        return reverse_transaction

    def set_expiry(self, days_from_now: int) -> None:
        """Set expiry date for earned points."""
        if self.is_earning_transaction:
            self.expires_at = datetime.utcnow().replace(day=datetime.utcnow().day + days_from_now)

    def expire(self) -> None:
        """Mark points as expired."""
        self.is_expired = True
        self.status = TransactionStatus.COMPLETED

    def update_metadata(self, key: str, value: str) -> None:
        """Update metadata with key-value pair."""
        import json

        metadata = {}
        if self.metadata:
            try:
                metadata = json.loads(self.metadata)
            except json.JSONDecodeError:
                metadata = {}

        metadata[key] = value
        self.metadata = json.dumps(metadata)

    def get_metadata(self, key: str) -> str:
        """Get metadata value by key."""
        import json

        if not self.metadata:
            return None

        try:
            metadata = json.loads(self.metadata)
            return metadata.get(key)
        except json.JSONDecodeError:
            return None

    @classmethod
    def create_earning_transaction(
        cls,
        user_id: int,
        points: int,
        source: TransactionSource,
        description: str,
        campaign_id: int = None,
        expires_in_days: int = 365,
        reference_id: str = None,
        reference_type: str = None
    ) -> 'PointTransaction':
        """
        Create a new point earning transaction.

        Args:
            user_id: User ID
            points: Number of points to award (positive)
            source: Source of the points
            description: Transaction description
            campaign_id: Associated campaign ID
            expires_in_days: Days until points expire
            reference_id: External reference ID
            reference_type: Type of external reference

        Returns:
            PointTransaction: New earning transaction
        """
        transaction = cls(
            user_id=user_id,
            transaction_type=TransactionType.EARNED,
            source=source,
            points=abs(points),  # Ensure positive
            description=description,
            campaign_id=campaign_id,
            reference_id=reference_id,
            reference_type=reference_type
        )

        # Set expiry
        if expires_in_days > 0:
            transaction.set_expiry(expires_in_days)

        return transaction

    @classmethod
    def create_spending_transaction(
        cls,
        user_id: int,
        points: int,
        source: TransactionSource,
        description: str,
        reference_id: str = None,
        reference_type: str = None
    ) -> 'PointTransaction':
        """
        Create a new point spending transaction.

        Args:
            user_id: User ID
            points: Number of points to deduct (positive, will be made negative)
            source: Source of the spending
            description: Transaction description
            reference_id: External reference ID
            reference_type: Type of external reference

        Returns:
            PointTransaction: New spending transaction
        """
        return cls(
            user_id=user_id,
            transaction_type=TransactionType.SPENT,
            source=source,
            points=-abs(points),  # Ensure negative
            description=description,
            reference_id=reference_id,
            reference_type=reference_type
        )
