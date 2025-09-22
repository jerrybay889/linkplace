"""
포인트 관련 Pydantic 스키마
"""

from pydantic import BaseModel
from typing import List, Optional


class PointCreate(BaseModel):
    """포인트 거래 생성 요청"""
    points: int
    source: str  # review_write, campaign_participate, coupon_purchase 등
    source_id: int  # 관련 항목의 ID
    description: Optional[str] = None


class PointTransaction(BaseModel):
    """포인트 거래 내역"""
    id: int
    user_email: str
    transaction_type: str  # earned, used, expired
    points: int
    source: str
    source_id: int
    description: str
    status: str  # pending, completed, failed
    expires_at: Optional[str] = None
    created_at: str


class PointBalance(BaseModel):
    """포인트 잔액"""
    user_email: str
    total_points: int
    available_points: int
    pending_points: int
    used_points: int
    expired_points: int
    last_updated: str


class PointHistory(BaseModel):
    """포인트 거래 내역 목록"""
    transactions: List[PointTransaction]
    total: int
    page: int
    size: int
    pages: int


class PointResponse(BaseModel):
    """포인트 거래 응답"""
    transaction_id: int
    message: str
    points: int
    new_balance: int
