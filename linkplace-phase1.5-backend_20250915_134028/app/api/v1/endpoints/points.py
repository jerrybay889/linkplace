"""
포인트 관련 API 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
import logging
from datetime import datetime, timedelta

from app.schemas.points import PointTransaction, PointCreate, PointResponse, PointBalance, PointHistory
from app.api.v1.endpoints.auth import verify_token

router = APIRouter()
logger = logging.getLogger(__name__)

# 임시 포인트 데이터
fake_points_db = {
    "admin@linkplace.com": {
        "user_email": "admin@linkplace.com",
        "total_points": 1500,
        "available_points": 1200,
        "pending_points": 300,
        "used_points": 800,
        "expired_points": 0,
        "last_updated": datetime.now().isoformat()
    },
    "user1@example.com": {
        "user_email": "user1@example.com",
        "total_points": 850,
        "available_points": 650,
        "pending_points": 200,
        "used_points": 350,
        "expired_points": 50,
        "last_updated": datetime.now().isoformat()
    }
}

# 임시 포인트 거래 내역
fake_transactions_db = {
    1: {
        "id": 1,
        "user_email": "admin@linkplace.com",
        "transaction_type": "earned",
        "points": 500,
        "source": "review_write",
        "source_id": 1,
        "description": "리뷰 작성으로 포인트 적립",
        "status": "completed",
        "expires_at": (datetime.now() + timedelta(days=365)).isoformat(),
        "created_at": datetime.now().isoformat()
    },
    2: {
        "id": 2,
        "user_email": "admin@linkplace.com",
        "transaction_type": "used",
        "points": -200,
        "source": "coupon_purchase",
        "source_id": 10,
        "description": "쿠폰 구매로 포인트 사용",
        "status": "completed",
        "expires_at": None,
        "created_at": (datetime.now() - timedelta(days=1)).isoformat()
    },
    3: {
        "id": 3,
        "user_email": "user1@example.com",
        "transaction_type": "earned",
        "points": 300,
        "source": "campaign_participate",
        "source_id": 5,
        "description": "캠페인 참여로 포인트 적립",
        "status": "pending",
        "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
        "created_at": datetime.now().isoformat()
    }
}


@router.get("/balance", response_model=PointBalance)
async def get_point_balance(current_user: str = Depends(verify_token)):
    """사용자 포인트 잔액 조회"""
    balance = fake_points_db.get(current_user)

    if not balance:
        # 새 사용자인 경우 초기 잔액 생성
        balance = {
            "user_email": current_user,
            "total_points": 0,
            "available_points": 0,
            "pending_points": 0,
            "used_points": 0,
            "expired_points": 0,
            "last_updated": datetime.now().isoformat()
        }
        fake_points_db[current_user] = balance

    return PointBalance(**balance)


@router.get("/history", response_model=PointHistory)
async def get_point_history(
    current_user: str = Depends(verify_token),
    transaction_type: Optional[str] = Query(None, description="거래 유형 (earned, used, expired)"),
    source: Optional[str] = Query(None, description="포인트 획득/사용 소스"),
    status: Optional[str] = Query(None, description="거래 상태 (pending, completed, failed)"),
    start_date: Optional[str] = Query(None, description="시작 날짜 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="종료 날짜 (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기")
):
    """포인트 거래 내역 조회"""
    # 사용자의 거래 내역만 필터
    transactions = [t for t in fake_transactions_db.values() if t["user_email"] == current_user]

    # 필터 적용
    if transaction_type:
        transactions = [t for t in transactions if t["transaction_type"] == transaction_type]

    if source:
        transactions = [t for t in transactions if t["source"] == source]

    if status:
        transactions = [t for t in transactions if t["status"] == status]

    if start_date:
        transactions = [t for t in transactions if t["created_at"].split("T")[0] >= start_date]

    if end_date:
        transactions = [t for t in transactions if t["created_at"].split("T")[0] <= end_date]

    # 최신순 정렬
    transactions.sort(key=lambda x: x["created_at"], reverse=True)

    # 페이지네이션
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    paginated_transactions = transactions[start_idx:end_idx]

    return PointHistory(
        transactions=[PointTransaction(**t) for t in paginated_transactions],
        total=len(transactions),
        page=page,
        size=size,
        pages=(len(transactions) + size - 1) // size
    )


@router.post("/earn", response_model=PointResponse)
async def earn_points(
    point_data: PointCreate,
    current_user: str = Depends(verify_token)
):
    """포인트 적립"""
    # 새 거래 ID 생성
    new_id = max(fake_transactions_db.keys()) + 1 if fake_transactions_db else 1

    # 새 거래 생성
    new_transaction = {
        "id": new_id,
        "user_email": current_user,
        "transaction_type": "earned",
        "points": point_data.points,
        "source": point_data.source,
        "source_id": point_data.source_id,
        "description": point_data.description or f"{point_data.source}로 포인트 적립",
        "status": "pending",  # 적립 포인트는 일반적으로 검토 후 승인
        "expires_at": (datetime.now() + timedelta(days=365)).isoformat(),
        "created_at": datetime.now().isoformat()
    }

    fake_transactions_db[new_id] = new_transaction

    # 사용자 포인트 잔액 업데이트
    if current_user not in fake_points_db:
        fake_points_db[current_user] = {
            "user_email": current_user,
            "total_points": 0,
            "available_points": 0,
            "pending_points": 0,
            "used_points": 0,
            "expired_points": 0,
            "last_updated": datetime.now().isoformat()
        }

    balance = fake_points_db[current_user]
    balance["pending_points"] += point_data.points
    balance["last_updated"] = datetime.now().isoformat()

    logger.info(f"Points earned: {point_data.points} for {current_user} from {point_data.source}")

    return PointResponse(
        transaction_id=new_id,
        message="포인트가 적립 요청되었습니다. 검토 후 승인됩니다.",
        points=point_data.points,
        new_balance=balance["available_points"] + balance["pending_points"]
    )


@router.post("/use", response_model=PointResponse)
async def use_points(
    point_data: PointCreate,
    current_user: str = Depends(verify_token)
):
    """포인트 사용"""
    # 사용자 잔액 확인
    balance = fake_points_db.get(current_user)

    if not balance or balance["available_points"] < point_data.points:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient points"
        )

    # 새 거래 ID 생성
    new_id = max(fake_transactions_db.keys()) + 1 if fake_transactions_db else 1

    # 새 거래 생성
    new_transaction = {
        "id": new_id,
        "user_email": current_user,
        "transaction_type": "used",
        "points": -point_data.points,  # 사용은 음수
        "source": point_data.source,
        "source_id": point_data.source_id,
        "description": point_data.description or f"{point_data.source}로 포인트 사용",
        "status": "completed",
        "expires_at": None,
        "created_at": datetime.now().isoformat()
    }

    fake_transactions_db[new_id] = new_transaction

    # 사용자 포인트 잔액 업데이트
    balance["available_points"] -= point_data.points
    balance["used_points"] += point_data.points
    balance["last_updated"] = datetime.now().isoformat()

    logger.info(f"Points used: {point_data.points} by {current_user} for {point_data.source}")

    return PointResponse(
        transaction_id=new_id,
        message="포인트가 사용되었습니다.",
        points=point_data.points,
        new_balance=balance["available_points"]
    )


@router.post("/approve/{transaction_id}")
async def approve_transaction(
    transaction_id: int,
    current_user: str = Depends(verify_token)
):
    """포인트 거래 승인 (관리자 전용)"""
    transaction = fake_transactions_db.get(transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    if transaction["status"] != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction is not pending"
        )

    # 거래 승인
    transaction["status"] = "completed"

    # 사용자 잔액 업데이트 (적립의 경우)
    if transaction["transaction_type"] == "earned":
        user_email = transaction["user_email"]
        balance = fake_points_db.get(user_email)

        if balance:
            balance["available_points"] += transaction["points"]
            balance["pending_points"] -= transaction["points"]
            balance["total_points"] += transaction["points"]
            balance["last_updated"] = datetime.now().isoformat()

    logger.info(f"Transaction approved: {transaction_id} by {current_user}")

    return {"message": "Transaction approved successfully"}


@router.post("/reject/{transaction_id}")
async def reject_transaction(
    transaction_id: int,
    reason: str = Query(..., description="거부 사유"),
    current_user: str = Depends(verify_token)
):
    """포인트 거래 거부 (관리자 전용)"""
    transaction = fake_transactions_db.get(transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    if transaction["status"] != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction is not pending"
        )

    # 거래 거부
    transaction["status"] = "failed"
    transaction["description"] += f" (거부 사유: {reason})"

    # 사용자 잔액 업데이트 (대기 중인 포인트 제거)
    if transaction["transaction_type"] == "earned":
        user_email = transaction["user_email"]
        balance = fake_points_db.get(user_email)

        if balance:
            balance["pending_points"] -= transaction["points"]
            balance["last_updated"] = datetime.now().isoformat()

    logger.info(f"Transaction rejected: {transaction_id} by {current_user} (reason: {reason})")

    return {"message": "Transaction rejected successfully"}


@router.get("/expiring")
async def get_expiring_points(
    current_user: str = Depends(verify_token),
    days: int = Query(30, description="만료 예정일 (일)")
):
    """만료 예정 포인트 조회"""
    cutoff_date = (datetime.now() + timedelta(days=days)).isoformat()

    expiring_transactions = []
    for transaction in fake_transactions_db.values():
        if (transaction["user_email"] == current_user and 
            transaction["transaction_type"] == "earned" and 
            transaction["status"] == "completed" and
            transaction["expires_at"] and 
            transaction["expires_at"] <= cutoff_date):
            expiring_transactions.append(transaction)

    total_expiring_points = sum(t["points"] for t in expiring_transactions)

    return {
        "total_expiring_points": total_expiring_points,
        "expiring_transactions": expiring_transactions,
        "expires_within_days": days
    }


@router.get("/stats")
async def get_point_stats(current_user: str = Depends(verify_token)):
    """포인트 통계 조회"""
    user_transactions = [t for t in fake_transactions_db.values() if t["user_email"] == current_user]

    # 월별 포인트 적립/사용 통계
    monthly_stats = {}
    for transaction in user_transactions:
        month_key = transaction["created_at"][:7]  # YYYY-MM

        if month_key not in monthly_stats:
            monthly_stats[month_key] = {"earned": 0, "used": 0}

        if transaction["transaction_type"] == "earned" and transaction["status"] == "completed":
            monthly_stats[month_key]["earned"] += transaction["points"]
        elif transaction["transaction_type"] == "used":
            monthly_stats[month_key]["used"] += abs(transaction["points"])

    # 소스별 포인트 적립 통계
    source_stats = {}
    for transaction in user_transactions:
        if transaction["transaction_type"] == "earned" and transaction["status"] == "completed":
            source = transaction["source"]
            if source not in source_stats:
                source_stats[source] = 0
            source_stats[source] += transaction["points"]

    return {
        "monthly_stats": monthly_stats,
        "source_stats": source_stats,
        "total_transactions": len(user_transactions)
    }
