"""
Authentication dependencies and utilities for FastAPI.
Handles JWT token validation, user authentication, and authorization.
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.utils.jwt import decode_access_token

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash.

    Args:
        plain_password: The plain text password
        hashed_password: The hashed password from database

    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password for storing in the database.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Get user by email from database.

    Args:
        db: Database session
        email: User email address

    Returns:
        Optional[User]: User object if found, None otherwise
    """
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate user with email and password.

    Args:
        db: Database session
        email: User email
        password: Plain text password

    Returns:
        Optional[User]: Authenticated user if credentials are valid, None otherwise
    """
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.

    Args:
        credentials: HTTP Authorization header with Bearer token
        db: Database session

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Extract token from credentials
        token = credentials.credentials

        # Decode JWT token
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception

        # Get user email from token
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Get user from database
    user = await get_user_by_email(db, email=user_email)
    if user is None:
        raise credentials_exception

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user (alias for get_current_user with active check).

    Args:
        current_user: Current user from get_current_user dependency

    Returns:
        User: Current active user
    """
    return current_user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get current user optionally (returns None if no valid token provided).
    Used for endpoints that work both with and without authentication.

    Args:
        credentials: Optional HTTP Authorization header
        db: Database session

    Returns:
        Optional[User]: Current user if authenticated, None otherwise
    """
    if not credentials:
        return None

    try:
        token = credentials.credentials
        payload = decode_access_token(token)
        if payload is None:
            return None

        user_email: str = payload.get("sub")
        if user_email is None:
            return None

        user = await get_user_by_email(db, email=user_email)
        if user and user.is_active:
            return user

    except (JWTError, Exception):
        pass

    return None


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Require admin privileges for accessing endpoint.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current user if admin

    Raises:
        HTTPException: If user is not admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def require_merchant(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Require merchant privileges for accessing endpoint.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current user if merchant or admin

    Raises:
        HTTPException: If user is not merchant or admin
    """
    if current_user.user_type not in ["merchant", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Merchant privileges required"
        )
    return current_user
