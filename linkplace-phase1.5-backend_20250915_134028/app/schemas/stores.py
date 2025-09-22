"""
매장 관련 Pydantic 스키마
"""

from pydantic import BaseModel
from typing import List, Optional


class StoreCreate(BaseModel):
    """매장 생성 요청"""
    name: str
    category: str
    address: str
    phone: Optional[str] = None
    description: Optional[str] = None
    latitude: float
    longitude: float
    business_hours: Optional[str] = None


class StoreUpdate(BaseModel):
    """매장 수정 요청"""
    name: Optional[str] = None
    category: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    business_hours: Optional[str] = None


class StoreResponse(BaseModel):
    """매장 응답"""
    id: int
    name: str
    category: str
    address: str
    phone: Optional[str] = None
    description: Optional[str] = None
    latitude: float
    longitude: float
    business_hours: Optional[str] = None
    is_active: bool
    created_at: str
    updated_at: str
    rating: float
    review_count: int
    distance: Optional[float] = None


class StoreList(BaseModel):
    """매장 목록 응답"""
    stores: List[StoreResponse]
    total: int
    page: int
    size: int
    pages: int
