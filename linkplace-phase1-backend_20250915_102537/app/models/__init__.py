"""
Database models for LinkPlace backend.
Contains all SQLAlchemy model definitions and imports.
"""

from .user import User, UserType, SocialProvider
from .merchant import Merchant, MerchantStatus, BusinessType
from .store import Store, StoreStatus, StoreCategory
from .campaign import Campaign, CampaignStatus, CampaignType
from .review import Review, ReviewStatus, ReviewType
from .point_transaction import PointTransaction, TransactionType, TransactionSource, TransactionStatus

# Import the base for easier access
from app.core.database import Base

__all__ = [
    # Models
    "User",
    "Merchant", 
    "Store",
    "Campaign",
    "Review",
    "PointTransaction",

    # Enums
    "UserType",
    "SocialProvider",
    "MerchantStatus",
    "BusinessType",
    "StoreStatus",
    "StoreCategory", 
    "CampaignStatus",
    "CampaignType",
    "ReviewStatus",
    "ReviewType",
    "TransactionType",
    "TransactionSource",
    "TransactionStatus",

    # Base
    "Base",
]
