"""
Social authentication service for OAuth2 providers.
Handles integration with Naver, Google, and Kakao login services.
"""
import httpx
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, SocialProvider
from app.schemas.auth import SocialLoginData
from app.services.user_service import UserService
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class SocialAuthService:
    """Service for social authentication providers."""

    @staticmethod
    async def authenticate_with_provider(
        provider: SocialProvider,
        access_token: str
    ) -> SocialLoginData:
        """
        Authenticate with social provider and get user data.

        Args:
            provider: Social provider
            access_token: Access token from provider

        Returns:
            SocialLoginData: User data from provider

        Raises:
            HTTPException: If authentication fails
        """
        if provider == SocialProvider.NAVER:
            return await SocialAuthService._authenticate_naver(access_token)
        elif provider == SocialProvider.GOOGLE:
            return await SocialAuthService._authenticate_google(access_token)
        elif provider == SocialProvider.KAKAO:
            return await SocialAuthService._authenticate_kakao(access_token)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported social provider: {provider.value}"
            )

    @staticmethod
    async def _authenticate_naver(access_token: str) -> SocialLoginData:
        """
        Authenticate with Naver and get user profile.

        Args:
            access_token: Naver access token

        Returns:
            SocialLoginData: User data from Naver
        """
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {access_token}"}
                response = await client.get(
                    "https://openapi.naver.com/v1/nid/me",
                    headers=headers
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid Naver access token"
                    )

                data = response.json()
                if data.get("resultcode") != "00":
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Naver authentication failed"
                    )

                user_info = data.get("response", {})

                return SocialLoginData(
                    provider=SocialProvider.NAVER,
                    social_id=user_info.get("id"),
                    email=user_info.get("email"),
                    full_name=user_info.get("name"),
                    nickname=user_info.get("nickname"),
                    profile_image_url=user_info.get("profile_image")
                )

        except httpx.RequestError as e:
            logger.error(f"Naver API request failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Naver authentication service unavailable"
            )

    @staticmethod
    async def _authenticate_google(access_token: str) -> SocialLoginData:
        """
        Authenticate with Google and get user profile.

        Args:
            access_token: Google access token

        Returns:
            SocialLoginData: User data from Google
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}"
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid Google access token"
                    )

                user_info = response.json()

                return SocialLoginData(
                    provider=SocialProvider.GOOGLE,
                    social_id=user_info.get("id"),
                    email=user_info.get("email"),
                    full_name=user_info.get("name"),
                    nickname=user_info.get("name"),  # Google doesn't have separate nickname
                    profile_image_url=user_info.get("picture")
                )

        except httpx.RequestError as e:
            logger.error(f"Google API request failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Google authentication service unavailable"
            )

    @staticmethod
    async def _authenticate_kakao(access_token: str) -> SocialLoginData:
        """
        Authenticate with Kakao and get user profile.

        Args:
            access_token: Kakao access token

        Returns:
            SocialLoginData: User data from Kakao
        """
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {access_token}"}
                response = await client.get(
                    "https://kapi.kakao.com/v2/user/me",
                    headers=headers
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid Kakao access token"
                    )

                user_info = response.json()
                kakao_account = user_info.get("kakao_account", {})
                profile = kakao_account.get("profile", {})

                return SocialLoginData(
                    provider=SocialProvider.KAKAO,
                    social_id=str(user_info.get("id")),
                    email=kakao_account.get("email"),
                    full_name=profile.get("nickname"),
                    nickname=profile.get("nickname"),
                    profile_image_url=profile.get("profile_image_url")
                )

        except httpx.RequestError as e:
            logger.error(f"Kakao API request failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Kakao authentication service unavailable"
            )

    @staticmethod
    async def login_or_register_social_user(
        db: AsyncSession,
        social_data: SocialLoginData
    ) -> tuple[User, bool]:
        """
        Login existing social user or register new one.

        Args:
            db: Database session
            social_data: Social login data

        Returns:
            tuple: (User object, is_new_user boolean)

        Raises:
            HTTPException: If registration fails
        """
        # Try to find existing user by social ID
        existing_user = await UserService.get_user_by_social_id(
            db, social_data.provider, social_data.social_id
        )

        if existing_user:
            # Update user data from social provider
            if social_data.profile_image_url:
                existing_user.profile_image_url = social_data.profile_image_url
            if social_data.full_name and not existing_user.full_name:
                existing_user.full_name = social_data.full_name

            await UserService.update_last_login(db, existing_user)
            logger.info(f"Social login for existing user: {existing_user.email} (ID: {existing_user.id})")
            return existing_user, False

        # Check if user exists with same email but different provider
        if social_data.email:
            email_user = await UserService.get_user_by_email(db, social_data.email)
            if email_user and email_user.social_provider != social_data.provider:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Account with email {social_data.email} already exists with different login method"
                )

        # Create new user
        from app.schemas.user import UserCreate

        user_create = UserCreate(
            email=social_data.email or f"{social_data.social_id}@{social_data.provider.value}.linkplace.local",
            full_name=social_data.full_name,
            nickname=social_data.nickname,
            social_provider=social_data.provider,
            social_id=social_data.social_id,
            profile_image_url=social_data.profile_image_url,
            marketing_consent=False  # Default to False for social logins
        )

        new_user = await UserService.create_user(db, user_create)
        logger.info(f"Created new social user: {new_user.email} (ID: {new_user.id})")
        return new_user, True

    @staticmethod
    def generate_oauth_url(provider: SocialProvider, state: str = None) -> str:
        """
        Generate OAuth authorization URL for social provider.

        Args:
            provider: Social provider
            state: Optional state parameter

        Returns:
            str: Authorization URL
        """
        if provider == SocialProvider.NAVER:
            base_url = "https://nid.naver.com/oauth2.0/authorize"
            params = {
                "response_type": "code",
                "client_id": settings.naver_client_id,
                "redirect_uri": settings.naver_redirect_uri,
                "scope": "name,email,profile_image"
            }
        elif provider == SocialProvider.GOOGLE:
            base_url = "https://accounts.google.com/o/oauth2/auth"
            params = {
                "response_type": "code",
                "client_id": settings.google_client_id,
                "redirect_uri": settings.google_redirect_uri,
                "scope": "openid email profile"
            }
        elif provider == SocialProvider.KAKAO:
            base_url = "https://kauth.kakao.com/oauth/authorize"
            params = {
                "response_type": "code",
                "client_id": settings.kakao_client_id,
                "redirect_uri": settings.kakao_redirect_uri,
                "scope": "profile_nickname,profile_image,account_email"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported social provider: {provider.value}"
            )

        if state:
            params["state"] = state

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}"

    @staticmethod
    async def exchange_code_for_token(
        provider: SocialProvider,
        code: str
    ) -> str:
        """
        Exchange authorization code for access token.

        Args:
            provider: Social provider
            code: Authorization code

        Returns:
            str: Access token

        Raises:
            HTTPException: If token exchange fails
        """
        try:
            async with httpx.AsyncClient() as client:
                if provider == SocialProvider.NAVER:
                    token_url = "https://nid.naver.com/oauth2.0/token"
                    data = {
                        "grant_type": "authorization_code",
                        "client_id": settings.naver_client_id,
                        "client_secret": settings.naver_client_secret,
                        "code": code,
                        "redirect_uri": settings.naver_redirect_uri
                    }
                elif provider == SocialProvider.GOOGLE:
                    token_url = "https://oauth2.googleapis.com/token"
                    data = {
                        "grant_type": "authorization_code",
                        "client_id": settings.google_client_id,
                        "client_secret": settings.google_client_secret,
                        "code": code,
                        "redirect_uri": settings.google_redirect_uri
                    }
                elif provider == SocialProvider.KAKAO:
                    token_url = "https://kauth.kakao.com/oauth/token"
                    data = {
                        "grant_type": "authorization_code",
                        "client_id": settings.kakao_client_id,
                        "client_secret": settings.kakao_client_secret,
                        "code": code,
                        "redirect_uri": settings.kakao_redirect_uri
                    }
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Unsupported social provider: {provider.value}"
                    )

                response = await client.post(token_url, data=data)

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Failed to exchange code for token"
                    )

                token_data = response.json()
                access_token = token_data.get("access_token")

                if not access_token:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No access token received"
                    )

                return access_token

        except httpx.RequestError as e:
            logger.error(f"Token exchange request failed for {provider.value}: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"{provider.value} authentication service unavailable"
            )
