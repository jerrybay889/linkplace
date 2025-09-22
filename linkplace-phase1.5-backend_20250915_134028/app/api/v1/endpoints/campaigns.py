"""
캠페인 관련 API 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
import logging
from datetime import datetime, timedelta

from app.schemas.campaigns import CampaignCreate, CampaignUpdate, CampaignResponse, CampaignList, CampaignParticipation
from app.api.v1.endpoints.auth import verify_token

router = APIRouter()
logger = logging.getLogger(__name__)

# 임시 캠페인 데이터
fake_campaigns_db = {
    1: {
        "id": 1,
        "title": "신규 매장 리뷰 작성 이벤트",
        "description": "새로 오픈한 매장에 리뷰를 작성하면 추가 포인트를 드립니다!",
        "campaign_type": "review_bonus",
        "reward_type": "points",
        "reward_value": 500,
        "start_date": "2024-01-01T00:00:00",
        "end_date": "2024-03-31T23:59:59",
        "is_active": True,
        "max_participants": 1000,
        "current_participants": 45,
        "conditions": {
            "min_rating": 4,
            "min_content_length": 50,
            "target_stores": [1, 2, 3]
        },
        "created_at": "2023-12-15T10:00:00",
        "updated_at": "2024-01-10T15:30:00"
    },
    2: {
        "id": 2,
        "title": "사진 리뷰 챌린지",
        "description": "사진이 포함된 리뷰를 작성하면 특별 쿠폰을 드려요!",
        "campaign_type": "photo_review",
        "reward_type": "coupon",
        "reward_value": 1,
        "start_date": "2024-02-01T00:00:00",
        "end_date": "2024-02-29T23:59:59",
        "is_active": True,
        "max_participants": 500,
        "current_participants": 123,
        "conditions": {
            "requires_photo": True,
            "min_photos": 2,
            "min_rating": 3
        },
        "created_at": "2024-01-20T09:00:00",
        "updated_at": "2024-01-25T11:15:00"
    }
}

# 임시 캠페인 참여 데이터
fake_participations_db = {
    1: {
        "id": 1,
        "campaign_id": 1,
        "user_email": "admin@linkplace.com",
        "participation_date": "2024-01-15T14:30:00",
        "status": "completed",
        "reward_claimed": True,
        "reward_claimed_at": "2024-01-16T10:00:00",
        "submission_data": {
            "review_id": 1,
            "store_id": 1
        }
    },
    2: {
        "id": 2,
        "campaign_id": 2,
        "user_email": "user1@example.com",
        "participation_date": "2024-02-05T16:20:00",
        "status": "pending_review",
        "reward_claimed": False,
        "reward_claimed_at": None,
        "submission_data": {
            "review_id": 2,
            "store_id": 1,
            "photo_count": 3
        }
    }
}


@router.get("/", response_model=CampaignList)
async def get_campaigns(
    campaign_type: Optional[str] = Query(None, description="캠페인 유형 필터"),
    is_active: Optional[bool] = Query(None, description="활성 상태 필터"),
    reward_type: Optional[str] = Query(None, description="보상 유형 필터 (points, coupon)"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기")
):
    """캠페인 목록 조회"""
    campaigns = list(fake_campaigns_db.values())

    # 필터 적용
    if campaign_type:
        campaigns = [c for c in campaigns if c["campaign_type"] == campaign_type]

    if is_active is not None:
        campaigns = [c for c in campaigns if c["is_active"] == is_active]

    if reward_type:
        campaigns = [c for c in campaigns if c["reward_type"] == reward_type]

    # 현재 시간 기준으로 활성 캠페인 확인
    now = datetime.now().isoformat()
    for campaign in campaigns:
        if campaign["start_date"] <= now <= campaign["end_date"]:
            campaign["status"] = "active"
        elif now < campaign["start_date"]:
            campaign["status"] = "upcoming"
        else:
            campaign["status"] = "ended"

    # 최신순 정렬
    campaigns.sort(key=lambda x: x["created_at"], reverse=True)

    # 페이지네이션
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    paginated_campaigns = campaigns[start_idx:end_idx]

    return CampaignList(
        campaigns=[CampaignResponse(**campaign) for campaign in paginated_campaigns],
        total=len(campaigns),
        page=page,
        size=size,
        pages=(len(campaigns) + size - 1) // size
    )


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: int):
    """특정 캠페인 조회"""
    campaign = fake_campaigns_db.get(campaign_id)

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # 상태 설정
    now = datetime.now().isoformat()
    if campaign["start_date"] <= now <= campaign["end_date"]:
        campaign["status"] = "active"
    elif now < campaign["start_date"]:
        campaign["status"] = "upcoming"
    else:
        campaign["status"] = "ended"

    return CampaignResponse(**campaign)


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user: str = Depends(verify_token)
):
    """새 캠페인 생성"""
    # 새 캠페인 ID 생성
    new_id = max(fake_campaigns_db.keys()) + 1 if fake_campaigns_db else 1

    # 현재 시간
    now = datetime.now().isoformat()

    # 새 캠페인 데이터
    new_campaign = {
        "id": new_id,
        **campaign_data.dict(),
        "current_participants": 0,
        "created_at": now,
        "updated_at": now
    }

    fake_campaigns_db[new_id] = new_campaign

    logger.info(f"Campaign created: {new_campaign['title']} by {current_user}")

    return CampaignResponse(**new_campaign)


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: int,
    campaign_data: CampaignUpdate,
    current_user: str = Depends(verify_token)
):
    """캠페인 수정"""
    campaign = fake_campaigns_db.get(campaign_id)

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # 업데이트할 데이터만 적용
    update_data = campaign_data.dict(exclude_unset=True)

    if update_data:
        campaign.update(update_data)
        campaign["updated_at"] = datetime.now().isoformat()

        logger.info(f"Campaign updated: {campaign_id} by {current_user}")

    return CampaignResponse(**campaign)


@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: int,
    current_user: str = Depends(verify_token)
):
    """캠페인 삭제 (비활성화)"""
    campaign = fake_campaigns_db.get(campaign_id)

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # 실제로는 삭제하지 않고 비활성화
    campaign["is_active"] = False
    campaign["updated_at"] = datetime.now().isoformat()

    logger.info(f"Campaign deactivated: {campaign_id} by {current_user}")

    return {"message": "Campaign deleted successfully"}


@router.post("/{campaign_id}/participate")
async def participate_campaign(
    campaign_id: int,
    submission_data: dict,
    current_user: str = Depends(verify_token)
):
    """캠페인 참여"""
    campaign = fake_campaigns_db.get(campaign_id)

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    if not campaign["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campaign is not active"
        )

    # 캠페인 기간 확인
    now = datetime.now().isoformat()
    if not (campaign["start_date"] <= now <= campaign["end_date"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campaign is not currently running"
        )

    # 최대 참여자 수 확인
    if (campaign.get("max_participants") and 
        campaign["current_participants"] >= campaign["max_participants"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campaign has reached maximum participants"
        )

    # 중복 참여 확인
    existing_participation = any(
        p["campaign_id"] == campaign_id and p["user_email"] == current_user
        for p in fake_participations_db.values()
    )

    if existing_participation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already participated in this campaign"
        )

    # 새 참여 ID 생성
    new_id = max(fake_participations_db.keys()) + 1 if fake_participations_db else 1

    # 참여 데이터 생성
    new_participation = {
        "id": new_id,
        "campaign_id": campaign_id,
        "user_email": current_user,
        "participation_date": datetime.now().isoformat(),
        "status": "pending_review",
        "reward_claimed": False,
        "reward_claimed_at": None,
        "submission_data": submission_data
    }

    fake_participations_db[new_id] = new_participation

    # 캠페인 참여자 수 증가
    campaign["current_participants"] += 1
    campaign["updated_at"] = datetime.now().isoformat()

    logger.info(f"Campaign participation: {campaign_id} by {current_user}")

    return {
        "message": "Campaign participation successful",
        "participation_id": new_id,
        "status": "pending_review"
    }


@router.get("/{campaign_id}/participants")
async def get_campaign_participants(
    campaign_id: int,
    current_user: str = Depends(verify_token),
    status: Optional[str] = Query(None, description="참여 상태 필터"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기")
):
    """캠페인 참여자 목록 조회 (관리자 전용)"""
    campaign = fake_campaigns_db.get(campaign_id)

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )

    # 참여자 목록 조회
    participants = [p for p in fake_participations_db.values() if p["campaign_id"] == campaign_id]

    # 상태 필터
    if status:
        participants = [p for p in participants if p["status"] == status]

    # 최신순 정렬
    participants.sort(key=lambda x: x["participation_date"], reverse=True)

    # 페이지네이션
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    paginated_participants = participants[start_idx:end_idx]

    return {
        "campaign_id": campaign_id,
        "participants": [CampaignParticipation(**p) for p in paginated_participants],
        "total": len(participants),
        "page": page,
        "size": size,
        "pages": (len(participants) + size - 1) // size
    }


@router.post("/participations/{participation_id}/approve")
async def approve_participation(
    participation_id: int,
    current_user: str = Depends(verify_token)
):
    """캠페인 참여 승인 (관리자 전용)"""
    participation = fake_participations_db.get(participation_id)

    if not participation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participation not found"
        )

    if participation["status"] != "pending_review":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Participation is not pending review"
        )

    # 참여 승인
    participation["status"] = "completed"

    logger.info(f"Campaign participation approved: {participation_id} by {current_user}")

    return {"message": "Participation approved successfully"}


@router.post("/participations/{participation_id}/reject")
async def reject_participation(
    participation_id: int,
    reason: str = Query(..., description="거부 사유"),
    current_user: str = Depends(verify_token)
):
    """캠페인 참여 거부 (관리자 전용)"""
    participation = fake_participations_db.get(participation_id)

    if not participation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participation not found"
        )

    if participation["status"] != "pending_review":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Participation is not pending review"
        )

    # 참여 거부
    participation["status"] = "rejected"
    participation["rejection_reason"] = reason

    logger.info(f"Campaign participation rejected: {participation_id} by {current_user} (reason: {reason})")

    return {"message": "Participation rejected successfully"}


@router.post("/participations/{participation_id}/claim-reward")
async def claim_reward(
    participation_id: int,
    current_user: str = Depends(verify_token)
):
    """캠페인 보상 수령"""
    participation = fake_participations_db.get(participation_id)

    if not participation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participation not found"
        )

    # 참여자 본인만 보상 수령 가능
    if participation["user_email"] != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    if participation["status"] != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Participation is not completed"
        )

    if participation["reward_claimed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reward already claimed"
        )

    # 보상 수령 처리
    participation["reward_claimed"] = True
    participation["reward_claimed_at"] = datetime.now().isoformat()

    campaign = fake_campaigns_db[participation["campaign_id"]]

    logger.info(f"Campaign reward claimed: {participation_id} by {current_user}")

    return {
        "message": "Reward claimed successfully",
        "reward_type": campaign["reward_type"],
        "reward_value": campaign["reward_value"]
    }


@router.get("/my-participations")
async def get_my_participations(
    current_user: str = Depends(verify_token),
    status: Optional[str] = Query(None, description="참여 상태 필터"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기")
):
    """내 캠페인 참여 내역 조회"""
    # 사용자의 참여 내역만 필터
    participations = [p for p in fake_participations_db.values() if p["user_email"] == current_user]

    # 상태 필터
    if status:
        participations = [p for p in participations if p["status"] == status]

    # 최신순 정렬
    participations.sort(key=lambda x: x["participation_date"], reverse=True)

    # 페이지네이션
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    paginated_participations = participations[start_idx:end_idx]

    # 캠페인 정보 포함
    for participation in paginated_participations:
        campaign = fake_campaigns_db.get(participation["campaign_id"])
        if campaign:
            participation["campaign_title"] = campaign["title"]
            participation["campaign_reward_type"] = campaign["reward_type"]
            participation["campaign_reward_value"] = campaign["reward_value"]

    return {
        "participations": [CampaignParticipation(**p) for p in paginated_participations],
        "total": len(participations),
        "page": page,
        "size": size,
        "pages": (len(participations) + size - 1) // size
    }
