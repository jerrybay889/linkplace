"""
JWT token utilities for authentication.
Handles token creation, validation, and decoding.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from app.core.config import settings


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Payload data to encode in the token
        expires_delta: Optional token expiration time delta

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.jwt_secret_key, 
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token with longer expiration.

    Args:
        data: Payload data to encode in the token
        expires_delta: Optional token expiration time delta

    Returns:
        str: Encoded JWT refresh token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Refresh tokens expire after 7 days by default
        expire = datetime.utcnow() + timedelta(days=7)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT access token.

    Args:
        token: JWT token to decode

    Returns:
        Optional[Dict[str, Any]]: Decoded payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        # Check if token is not a refresh token
        if payload.get("type") == "refresh":
            return None

        return payload

    except JWTError:
        return None


def decode_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT refresh token.

    Args:
        token: JWT refresh token to decode

    Returns:
        Optional[Dict[str, Any]]: Decoded payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        # Check if token is specifically a refresh token
        if payload.get("type") != "refresh":
            return None

        return payload

    except JWTError:
        return None


def verify_token(token: str) -> bool:
    """
    Verify if a JWT token is valid without decoding the payload.

    Args:
        token: JWT token to verify

    Returns:
        bool: True if token is valid, False otherwise
    """
    try:
        jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return True
    except JWTError:
        return False


def get_token_expiry(token: str) -> Optional[datetime]:
    """
    Get the expiration time of a JWT token.

    Args:
        token: JWT token to check

    Returns:
        Optional[datetime]: Token expiration time if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            return datetime.fromtimestamp(exp_timestamp)
        return None
    except JWTError:
        return None


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired.

    Args:
        token: JWT token to check

    Returns:
        bool: True if token is expired, False if valid
    """
    expiry = get_token_expiry(token)
    if expiry is None:
        return True  # Invalid token is considered expired

    return datetime.utcnow() > expiry


def create_password_reset_token(email: str) -> str:
    """
    Create a special JWT token for password reset.

    Args:
        email: User email for password reset

    Returns:
        str: JWT token for password reset (expires in 1 hour)
    """
    expires_delta = timedelta(hours=1)
    data = {"sub": email, "type": "password_reset"}
    return create_access_token(data, expires_delta)


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verify and decode a password reset token.

    Args:
        token: Password reset token

    Returns:
        Optional[str]: User email if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        # Check if token is specifically for password reset
        if payload.get("type") != "password_reset":
            return None

        email = payload.get("sub")
        return email

    except JWTError:
        return None
