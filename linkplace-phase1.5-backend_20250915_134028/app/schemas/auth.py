"""
인증 관련 Pydantic 스키마
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserLogin(BaseModel):
    """사용자 로그인 요청"""
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """사용자 회원가입 요청"""
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    """사용자 정보 응답"""
    id: int
    email: str
    username: str
    is_active: bool
    role: str


class Token(BaseModel):
    """토큰 응답"""
    access_token: str
    token_type: str
