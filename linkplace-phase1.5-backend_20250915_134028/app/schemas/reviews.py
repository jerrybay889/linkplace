"""
리뷰 관련 Pydantic 스키마
"""

from pydantic import BaseModel
from typing import List, Optional


class ReviewCreate(BaseModel):
    """리뷰 생성 요청"""
    store_id: int
    rating: int  # 1-5 별점
    title: str
    content: str
    images: Optional[List[str]] = []
    is_anonymous: Optional[bool] = False


class ReviewUpdate(BaseModel):
    """리뷰 수정 요청"""
    rating: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    images: Optional[List[str]] = None
    is_anonymous: Optional[bool] = None


class ReviewResponse(BaseModel):
    """리뷰 응답"""
    id: int
    store_id: int
    user_email: str
    rating: int
    title: str
    content: str
    images: List[str]
    is_anonymous: bool
    created_at: str
    updated_at: str
    likes: int
    helpful_count: int


class ReviewList(BaseModel):
    """리뷰 목록 응답"""
    reviews: List[ReviewResponse]
    total: int
    page: int
    size: int
    pages: int
