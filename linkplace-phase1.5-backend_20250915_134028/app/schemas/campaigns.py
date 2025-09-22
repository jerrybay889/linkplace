"""
캠페인 관련 Pydantic 스키마
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class CampaignCreate(BaseModel):
    """캠페인 생성 요청"""
    title: str
    description: str
    campaign_type: str  # review_bonus, photo_review, check_in 등
    reward_type: str  # points, coupon, discount
    reward_value: int
    start_date: str
    end_date: str
    is_active: bool = True
    max_participants: Optional[int] = None
    conditions: Optional[Dict[str, Any]] = {}


class CampaignUpdate(BaseModel):
    """캠페인 수정 요청"""
    title: Optional[str] = None
    description: Optional[str] = None
    campaign_type: Optional[str] = None
    reward_type: Optional[str] = None
    reward_value: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_active: Optional[bool] = None
    max_participants: Optional[int] = None
    conditions: Optional[Dict[str, Any]] = None


class CampaignResponse(BaseModel):
    """캠페인 응답"""
    id: int
    title: str
    description: str
    campaign_type: str
    reward_type: str
    reward_value: int
    start_date: str
    end_date: str
    is_active: bool
    max_participants: Optional[int] = None
    current_participants: int
    conditions: Dict[str, Any]
    created_at: str
    updated_at: str
    status: Optional[str] = None  # active, upcoming, ended


class CampaignList(BaseModel):
    """캠페인 목록 응답"""
    campaigns: List[CampaignResponse]
    total: int
    page: int
    size: int
    pages: int


class CampaignParticipation(BaseModel):
    """캠페인 참여 내역"""
    id: int
    campaign_id: int
    user_email: str
    participation_date: str
    status: str  # pending_review, completed, rejected
    reward_claimed: bool
    reward_claimed_at: Optional[str] = None
    submission_data: Dict[str, Any]
    campaign_title: Optional[str] = None
    campaign_reward_type: Optional[str] = None
    campaign_reward_value: Optional[int] = None
    rejection_reason: Optional[str] = None
