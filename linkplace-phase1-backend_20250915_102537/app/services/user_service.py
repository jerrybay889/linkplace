"""
User service layer for business logic.
Handles user registration, profile management, and user operations.
"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.user import User, UserType, SocialProvider
from app.schemas.user import UserCreate, UserUpdate
from app.core.auth import get_password_hash, verify_password
from app.utils.jwt import create_access_token, create_refresh_token
import logging

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user-related business logic."""

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """
        Create a new user.

        Args:
            db: Database session
            user_data: User creation data

        Returns:
            User: Created user object

        Raises:
            HTTPException: If user already exists or creation fails
        """
        # Check if user already exists
        existing_user = await UserService.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Check for social login duplicate
        if user_data.social_provider != SocialProvider.EMAIL and user_data.social_id:
            existing_social = await UserService.get_user_by_social_id(
                db, user_data.social_provider, user_data.social_id
            )
            if existing_social:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User with {user_data.social_provider.value} ID already exists"
                )

        # Hash password if provided
        hashed_password = None
        if user_data.password:
            hashed_password = get_password_hash(user_data.password)

        # Create user
        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            nickname=user_data.nickname,
            phone_number=user_data.phone_number,
            bio=user_data.bio,
            hashed_password=hashed_password,
            user_type=user_data.user_type,
            social_provider=user_data.social_provider,
            social_id=user_data.social_id,
            profile_image_url=user_data.profile_image_url,
            marketing_consent=user_data.marketing_consent,
            is_verified=user_data.social_provider != SocialProvider.EMAIL  # Auto-verify social logins
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        logger.info(f"Created new user: {user.email} (ID: {user.id})")
        return user

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email address."""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_social_id(
        db: AsyncSession, 
        provider: SocialProvider, 
        social_id: str
    ) -> Optional[User]:
        """Get user by social provider and social ID."""
        result = await db.execute(
            select(User).where(
                and_(
                    User.social_provider == provider,
                    User.social_id == social_id
                )
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_user(
        db: AsyncSession, 
        user: User, 
        update_data: UserUpdate
    ) -> User:
        """
        Update user profile.

        Args:
            db: Database session
            user: User to update
            update_data: Update data

        Returns:
            User: Updated user object
        """
        update_dict = update_data.dict(exclude_unset=True)

        for field, value in update_dict.items():
            setattr(user, field, value)

        user.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(user)

        logger.info(f"Updated user profile: {user.email} (ID: {user.id})")
        return user

    @staticmethod
    async def change_password(
        db: AsyncSession,
        user: User,
        current_password: str,
        new_password: str
    ) -> bool:
        """
        Change user password.

        Args:
            db: Database session
            user: User object
            current_password: Current password
            new_password: New password

        Returns:
            bool: True if successful

        Raises:
            HTTPException: If current password is incorrect
        """
        if not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot change password for social login accounts"
            )

        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )

        user.hashed_password = get_password_hash(new_password)
        user.updated_at = datetime.utcnow()

        await db.commit()

        logger.info(f"Password changed for user: {user.email} (ID: {user.id})")
        return True

    @staticmethod
    async def reset_password(db: AsyncSession, email: str, new_password: str) -> bool:
        """
        Reset user password (for password reset flow).

        Args:
            db: Database session
            email: User email
            new_password: New password

        Returns:
            bool: True if successful

        Raises:
            HTTPException: If user not found
        """
        user = await UserService.get_user_by_email(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.hashed_password = get_password_hash(new_password)
        user.updated_at = datetime.utcnow()

        await db.commit()

        logger.info(f"Password reset for user: {user.email} (ID: {user.id})")
        return True

    @staticmethod
    async def verify_email(db: AsyncSession, user: User) -> User:
        """
        Verify user email.

        Args:
            db: Database session
            user: User object

        Returns:
            User: Updated user object
        """
        user.mark_email_verified()
        await db.commit()
        await db.refresh(user)

        logger.info(f"Email verified for user: {user.email} (ID: {user.id})")
        return user

    @staticmethod
    async def deactivate_user(db: AsyncSession, user: User) -> User:
        """
        Deactivate user account.

        Args:
            db: Database session
            user: User object

        Returns:
            User: Updated user object
        """
        user.is_active = False
        user.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(user)

        logger.info(f"User deactivated: {user.email} (ID: {user.id})")
        return user

    @staticmethod
    async def activate_user(db: AsyncSession, user: User) -> User:
        """
        Activate user account.

        Args:
            db: Database session
            user: User object

        Returns:
            User: Updated user object
        """
        user.is_active = True
        user.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(user)

        logger.info(f"User activated: {user.email} (ID: {user.id})")
        return user

    @staticmethod
    async def update_last_login(db: AsyncSession, user: User) -> None:
        """
        Update user's last login timestamp.

        Args:
            db: Database session
            user: User object
        """
        user.update_last_login()
        await db.commit()

    @staticmethod
    async def search_users(
        db: AsyncSession,
        query: Optional[str] = None,
        user_type: Optional[UserType] = None,
        is_verified: Optional[bool] = None,
        is_active: Optional[bool] = None,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        page: int = 1,
        size: int = 10
    ) -> Dict[str, Any]:
        """
        Search users with filters and pagination.

        Args:
            db: Database session
            query: Search query
            user_type: Filter by user type
            is_verified: Filter by verification status
            is_active: Filter by active status
            created_after: Filter by creation date (after)
            created_before: Filter by creation date (before)
            page: Page number
            size: Page size

        Returns:
            Dict: Search results with pagination
        """
        # Build query
        stmt = select(User)
        conditions = []

        if query:
            conditions.append(
                or_(
                    User.email.ilike(f"%{query}%"),
                    User.full_name.ilike(f"%{query}%"),
                    User.nickname.ilike(f"%{query}%")
                )
            )

        if user_type is not None:
            conditions.append(User.user_type == user_type)

        if is_verified is not None:
            conditions.append(User.is_verified == is_verified)

        if is_active is not None:
            conditions.append(User.is_active == is_active)

        if created_after:
            conditions.append(User.created_at >= created_after)

        if created_before:
            conditions.append(User.created_at <= created_before)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        # Count total
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await db.execute(count_stmt)
        total = total_result.scalar()

        # Apply pagination
        offset = (page - 1) * size
        stmt = stmt.order_by(desc(User.created_at)).offset(offset).limit(size)

        # Execute query
        result = await db.execute(stmt)
        users = result.scalars().all()

        return {
            "users": users,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }

    @staticmethod
    async def get_user_stats(db: AsyncSession, user: User) -> Dict[str, Any]:
        """
        Get user statistics.

        Args:
            db: Database session
            user: User object

        Returns:
            Dict: User statistics
        """
        # This would typically involve complex queries across multiple tables
        # For now, return basic stats from user object
        return {
            "user_id": user.id,
            "total_points": user.total_points,
            "available_points": user.available_points,
            "member_since": user.created_at,
            "last_activity": user.last_login_at,
            "is_verified": user.is_verified,
            "user_type": user.user_type.value
        }

    @staticmethod
    async def check_nickname_availability(
        db: AsyncSession, 
        nickname: str, 
        exclude_user_id: Optional[int] = None
    ) -> bool:
        """
        Check if nickname is available.

        Args:
            db: Database session
            nickname: Nickname to check
            exclude_user_id: User ID to exclude from check

        Returns:
            bool: True if available, False if taken
        """
        stmt = select(User).where(User.nickname == nickname)

        if exclude_user_id:
            stmt = stmt.where(User.id != exclude_user_id)

        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        return existing_user is None
