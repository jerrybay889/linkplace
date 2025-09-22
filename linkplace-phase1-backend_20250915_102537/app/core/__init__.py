"""
Core module for LinkPlace backend.
Contains configuration, database, and authentication utilities.
"""

from .config import settings
from .database import get_db, Base, db_manager
from .auth import (
    get_current_user,
    get_current_active_user,
    get_current_user_optional,
    require_admin,
    require_merchant,
    verify_password,
    get_password_hash,
)

__all__ = [
    "settings",
    "get_db",
    "Base",
    "db_manager",
    "get_current_user",
    "get_current_active_user", 
    "get_current_user_optional",
    "require_admin",
    "require_merchant",
    "verify_password",
    "get_password_hash",
]
