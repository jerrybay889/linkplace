"""
Store model for physical locations.
Represents individual business locations managed by merchants.
"""
from datetime import datetime, time
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Numeric, Time, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class StoreStatus(enum.Enum):
    """Store status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    TEMPORARILY_CLOSED = "temporarily_closed"
    PERMANENTLY_CLOSED = "permanently_closed"
    PENDING_APPROVAL = "pending_approval"


class StoreCategory(enum.Enum):
    """Store category enumeration."""
    RESTAURANT = "restaurant"
    CAFE = "cafe"
    FAST_FOOD = "fast_food"
    RETAIL_CLOTHING = "retail_clothing"
    RETAIL_ELECTRONICS = "retail_electronics"
    RETAIL_GROCERY = "retail_grocery"
    BEAUTY_SALON = "beauty_salon"
    SPA = "spa"
    FITNESS_GYM = "fitness_gym"
    YOGA_STUDIO = "yoga_studio"
    BOOKSTORE = "bookstore"
    PHARMACY = "pharmacy"
    CONVENIENCE_STORE = "convenience_store"
    BAKERY = "bakery"
    OTHER = "other"


class Store(Base):
    """
    Store model for physical business locations.

    Represents individual stores that belong to merchants and can run campaigns.
    """
    __tablename__ = "stores"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False, index=True)

    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(Enum(StoreCategory), nullable=False)
    status = Column(Enum(StoreStatus), default=StoreStatus.PENDING_APPROVAL, nullable=False)

    # Location Information
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default="South Korea", nullable=False)

    # Geographic Coordinates
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)

    # Contact Information
    phone_number = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website_url = Column(String(500), nullable=True)

    # Business Hours (stored as JSON or structured format)
    monday_open = Column(Time, nullable=True)
    monday_close = Column(Time, nullable=True)
    tuesday_open = Column(Time, nullable=True)
    tuesday_close = Column(Time, nullable=True)
    wednesday_open = Column(Time, nullable=True)
    wednesday_close = Column(Time, nullable=True)
    thursday_open = Column(Time, nullable=True)
    thursday_close = Column(Time, nullable=True)
    friday_open = Column(Time, nullable=True)
    friday_close = Column(Time, nullable=True)
    saturday_open = Column(Time, nullable=True)
    saturday_close = Column(Time, nullable=True)
    sunday_open = Column(Time, nullable=True)
    sunday_close = Column(Time, nullable=True)

    # Store Details
    is_24_hours = Column(Boolean, default=False, nullable=False)
    has_parking = Column(Boolean, default=False, nullable=False)
    has_wifi = Column(Boolean, default=False, nullable=False)
    has_delivery = Column(Boolean, default=False, nullable=False)
    accepts_cards = Column(Boolean, default=True, nullable=False)
    wheelchair_accessible = Column(Boolean, default=False, nullable=False)

    # Visual Content
    logo_url = Column(Text, nullable=True)
    cover_image_url = Column(Text, nullable=True)
    gallery_images = Column(Text, nullable=True)  # JSON array of image URLs

    # Settings and Preferences
    allows_reviews = Column(Boolean, default=True, nullable=False)
    auto_approve_reviews = Column(Boolean, default=True, nullable=False)
    notification_email = Column(String(255), nullable=True)

    # Statistics and Performance
    total_campaigns = Column(Integer, default=0, nullable=False)
    active_campaigns = Column(Integer, default=0, nullable=False)
    total_visitors = Column(Integer, default=0, nullable=False)
    total_reviews = Column(Integer, default=0, nullable=False)
    average_rating = Column(Numeric(3, 2), default=0, nullable=False)

    # Social Media and Marketing
    instagram_url = Column(String(500), nullable=True)
    facebook_url = Column(String(500), nullable=True)
    twitter_url = Column(String(500), nullable=True)
    special_offers = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # JSON array of tags

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    approved_at = Column(DateTime, nullable=True)
    last_activity_at = Column(DateTime, nullable=True)

    # Relationships
    merchant = relationship("Merchant", back_populates="stores")
    campaigns = relationship("Campaign", back_populates="store", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="store", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Store(id={self.id}, name='{self.name}', status='{self.status.value}')>"

    @property
    def is_active(self) -> bool:
        """Check if store is active and operational."""
        return self.status == StoreStatus.ACTIVE

    @property
    def is_open_now(self) -> bool:
        """Check if store is currently open based on business hours."""
        if self.is_24_hours:
            return True

        now = datetime.now().time()
        today = datetime.now().weekday()  # 0=Monday, 6=Sunday

        # Get today's hours
        open_time = None
        close_time = None

        if today == 0:  # Monday
            open_time, close_time = self.monday_open, self.monday_close
        elif today == 1:  # Tuesday
            open_time, close_time = self.tuesday_open, self.tuesday_close
        elif today == 2:  # Wednesday
            open_time, close_time = self.wednesday_open, self.wednesday_close
        elif today == 3:  # Thursday
            open_time, close_time = self.thursday_open, self.thursday_close
        elif today == 4:  # Friday
            open_time, close_time = self.friday_open, self.friday_close
        elif today == 5:  # Saturday
            open_time, close_time = self.saturday_open, self.saturday_close
        elif today == 6:  # Sunday
            open_time, close_time = self.sunday_open, self.sunday_close

        if not open_time or not close_time:
            return False  # Closed today

        return open_time <= now <= close_time

    @property
    def display_address(self) -> str:
        """Get formatted address for display."""
        return f"{self.address}, {self.city}, {self.postal_code}"

    @property
    def coordinates(self) -> tuple:
        """Get latitude and longitude as tuple."""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None

    def approve(self) -> None:
        """Approve the store."""
        self.status = StoreStatus.ACTIVE
        self.approved_at = datetime.utcnow()

    def suspend(self) -> None:
        """Suspend the store temporarily."""
        self.status = StoreStatus.TEMPORARILY_CLOSED

    def close_permanently(self) -> None:
        """Close the store permanently."""
        self.status = StoreStatus.PERMANENTLY_CLOSED

    def reactivate(self) -> None:
        """Reactivate a suspended store."""
        if self.status == StoreStatus.TEMPORARILY_CLOSED:
            self.status = StoreStatus.ACTIVE

    def update_rating(self) -> None:
        """Update average rating based on reviews (should be called when reviews change)."""
        # This would typically calculate from related Review records
        pass

    def can_create_campaign(self) -> bool:
        """Check if store can create new campaigns."""
        return self.is_active and self.merchant.is_active

    def update_last_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity_at = datetime.utcnow()

    def set_coordinates(self, latitude: float, longitude: float) -> None:
        """Set store coordinates."""
        self.latitude = latitude
        self.longitude = longitude
