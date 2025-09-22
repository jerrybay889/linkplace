"""
아카이브 관련 API 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
import logging
from datetime import datetime, timedelta

from app.api.v1.endpoints.auth import verify_token

router = APIRouter()
logger = logging.getLogger(__name__)

# 임시 아카이브 데이터
fake_archive_db = {
    1: {
        "id": 1,
        "type": "review",
        "title": "강남 카페 리뷰",
        "content": "정말 좋은 카페였습니다...",
        "original_id": 1,
        "user_email": "user1@example.com",
        "archived_date": "2024-01-30T10:00:00",
        "archived_reason": "user_request",
        "metadata": {
            "store_id": 1,
            "store_name": "강남 카페",
            "rating": 5,
            "original_created_at": "2024-01-15T10:30:00"
        }
    },
    2: {
        "id": 2,
        "type": "campaign",
        "title": "종료된 겨울 이벤트",
        "content": "겨울 시즌 특별 캠페인...",
        "original_id": 10,
        "user_email": "admin@linkplace.com",
        "archived_date": "2024-02-29T23:59:59",
        "archived_reason": "expired",
        "metadata": {
            "campaign_type": "seasonal",
            "participants": 150,
            "original_start_date": "2023-12-01T00:00:00",
            "original_end_date": "2024-02-29T23:59:59"
        }
    }
}


@router.get("/", response_model=List[dict])
async def get_archived_items(
    item_type: Optional[str] = Query(None, description="아카이브 항목 유형 (review, campaign, store, user)"),
    user_email: Optional[str] = Query(None, description="사용자 이메일로 필터"),
    archived_reason: Optional[str] = Query(None, description="아카이브 사유 (user_request, expired, violation, admin_action)"),
    start_date: Optional[str] = Query(None, description="아카이브 시작 날짜 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="아카이브 종료 날짜 (YYYY-MM-DD)"),
    search: Optional[str] = Query(None, description="제목/내용 검색"),
    sort_by: str = Query("archived_date", description="정렬 기준 (archived_date, type, title)"),
    sort_order: str = Query("desc", description="정렬 순서 (asc, desc)"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    current_user: str = Depends(verify_token)
):
    """아카이브 항목 목록 조회"""
    items = list(fake_archive_db.values())

    # 필터 적용
    if item_type:
        items = [item for item in items if item["type"] == item_type]

    if user_email:
        items = [item for item in items if item["user_email"] == user_email]

    if archived_reason:
        items = [item for item in items if item["archived_reason"] == archived_reason]

    if start_date:
        items = [item for item in items if item["archived_date"].split("T")[0] >= start_date]

    if end_date:
        items = [item for item in items if item["archived_date"].split("T")[0] <= end_date]

    if search:
        search_lower = search.lower()
        items = [item for item in items 
                if search_lower in item["title"].lower() or 
                   search_lower in item["content"].lower()]

    # 정렬
    reverse_order = sort_order == "desc"
    if sort_by == "archived_date":
        items.sort(key=lambda x: x["archived_date"], reverse=reverse_order)
    elif sort_by == "type":
        items.sort(key=lambda x: x["type"], reverse=reverse_order)
    elif sort_by == "title":
        items.sort(key=lambda x: x["title"], reverse=reverse_order)

    # 페이지네이션
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    paginated_items = items[start_idx:end_idx]

    return {
        "items": paginated_items,
        "total": len(items),
        "page": page,
        "size": size,
        "pages": (len(items) + size - 1) // size
    }


@router.get("/{archive_id}")
async def get_archived_item(
    archive_id: int,
    current_user: str = Depends(verify_token)
):
    """특정 아카이브 항목 조회"""
    item = fake_archive_db.get(archive_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archived item not found"
        )

    return item


@router.post("/reviews/{review_id}")
async def archive_review(
    review_id: int,
    reason: str = Query(..., description="아카이브 사유"),
    current_user: str = Depends(verify_token)
):
    """리뷰 아카이브"""
    # 실제 구현에서는 reviews 테이블에서 해당 리뷰를 조회
    # 여기서는 임시 데이터로 시뮬레이션

    # 새 아카이브 ID 생성
    new_id = max(fake_archive_db.keys()) + 1 if fake_archive_db else 1

    # 아카이브 항목 생성
    archived_item = {
        "id": new_id,
        "type": "review",
        "title": f"리뷰 #{review_id}",
        "content": "아카이브된 리뷰 내용...",
        "original_id": review_id,
        "user_email": current_user,
        "archived_date": datetime.now().isoformat(),
        "archived_reason": reason,
        "metadata": {
            "archived_by": current_user,
            "original_created_at": "2024-01-15T10:30:00"
        }
    }

    fake_archive_db[new_id] = archived_item

    logger.info(f"Review archived: {review_id} by {current_user} (reason: {reason})")

    return {"message": "Review archived successfully", "archive_id": new_id}


@router.post("/campaigns/{campaign_id}")
async def archive_campaign(
    campaign_id: int,
    reason: str = Query(..., description="아카이브 사유"),
    current_user: str = Depends(verify_token)
):
    """캠페인 아카이브"""
    # 새 아카이브 ID 생성
    new_id = max(fake_archive_db.keys()) + 1 if fake_archive_db else 1

    # 아카이브 항목 생성
    archived_item = {
        "id": new_id,
        "type": "campaign",
        "title": f"캠페인 #{campaign_id}",
        "content": "아카이브된 캠페인 내용...",
        "original_id": campaign_id,
        "user_email": current_user,
        "archived_date": datetime.now().isoformat(),
        "archived_reason": reason,
        "metadata": {
            "archived_by": current_user,
            "original_created_at": "2024-01-01T00:00:00"
        }
    }

    fake_archive_db[new_id] = archived_item

    logger.info(f"Campaign archived: {campaign_id} by {current_user} (reason: {reason})")

    return {"message": "Campaign archived successfully", "archive_id": new_id}


@router.post("/stores/{store_id}")
async def archive_store(
    store_id: int,
    reason: str = Query(..., description="아카이브 사유"),
    current_user: str = Depends(verify_token)
):
    """매장 아카이브"""
    # 새 아카이브 ID 생성
    new_id = max(fake_archive_db.keys()) + 1 if fake_archive_db else 1

    # 아카이브 항목 생성
    archived_item = {
        "id": new_id,
        "type": "store",
        "title": f"매장 #{store_id}",
        "content": "아카이브된 매장 정보...",
        "original_id": store_id,
        "user_email": current_user,
        "archived_date": datetime.now().isoformat(),
        "archived_reason": reason,
        "metadata": {
            "archived_by": current_user,
            "original_created_at": "2024-01-01T00:00:00"
        }
    }

    fake_archive_db[new_id] = archived_item

    logger.info(f"Store archived: {store_id} by {current_user} (reason: {reason})")

    return {"message": "Store archived successfully", "archive_id": new_id}


@router.post("/{archive_id}/restore")
async def restore_archived_item(
    archive_id: int,
    current_user: str = Depends(verify_token)
):
    """아카이브 항목 복원"""
    item = fake_archive_db.get(archive_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archived item not found"
        )

    # 실제 구현에서는 원본 테이블에 데이터를 복원하고 아카이브에서 제거
    # 여기서는 시뮬레이션

    logger.info(f"Archive item restored: {archive_id} by {current_user}")

    return {
        "message": "Item restored successfully",
        "restored_type": item["type"],
        "original_id": item["original_id"]
    }


@router.delete("/{archive_id}")
async def permanently_delete_archived_item(
    archive_id: int,
    current_user: str = Depends(verify_token)
):
    """아카이브 항목 영구 삭제"""
    item = fake_archive_db.get(archive_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archived item not found"
        )

    # 아카이브에서 영구 삭제
    del fake_archive_db[archive_id]

    logger.info(f"Archive item permanently deleted: {archive_id} by {current_user}")

    return {"message": "Item permanently deleted"}


@router.get("/stats/summary")
async def get_archive_stats(current_user: str = Depends(verify_token)):
    """아카이브 통계 요약"""
    items = list(fake_archive_db.values())

    # 유형별 통계
    type_stats = {}
    for item in items:
        item_type = item["type"]
        if item_type not in type_stats:
            type_stats[item_type] = 0
        type_stats[item_type] += 1

    # 사유별 통계
    reason_stats = {}
    for item in items:
        reason = item["archived_reason"]
        if reason not in reason_stats:
            reason_stats[reason] = 0
        reason_stats[reason] += 1

    # 월별 아카이브 통계
    monthly_stats = {}
    for item in items:
        month_key = item["archived_date"][:7]  # YYYY-MM
        if month_key not in monthly_stats:
            monthly_stats[month_key] = 0
        monthly_stats[month_key] += 1

    # 최근 7일 아카이브 수
    seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
    recent_archives = [
        item for item in items 
        if item["archived_date"] >= seven_days_ago
    ]

    return {
        "total_archived_items": len(items),
        "type_distribution": type_stats,
        "reason_distribution": reason_stats,
        "monthly_stats": monthly_stats,
        "recent_7days_count": len(recent_archives),
        "oldest_archive_date": min([item["archived_date"] for item in items]) if items else None,
        "newest_archive_date": max([item["archived_date"] for item in items]) if items else None
    }


@router.post("/cleanup")
async def cleanup_old_archives(
    older_than_days: int = Query(365, description="삭제할 아카이브 보관 기간 (일)"),
    dry_run: bool = Query(True, description="실제 삭제하지 않고 미리보기만"),
    current_user: str = Depends(verify_token)
):
    """오래된 아카이브 항목 정리"""
    cutoff_date = (datetime.now() - timedelta(days=older_than_days)).isoformat()

    old_items = [
        item for item in fake_archive_db.values()
        if item["archived_date"] < cutoff_date
    ]

    if dry_run:
        return {
            "message": "Dry run completed",
            "items_to_delete": len(old_items),
            "cutoff_date": cutoff_date,
            "preview": old_items[:10]  # 처음 10개만 미리보기
        }
    else:
        # 실제 삭제
        deleted_count = 0
        for item in old_items:
            del fake_archive_db[item["id"]]
            deleted_count += 1

        logger.info(f"Archive cleanup: {deleted_count} items deleted by {current_user}")

        return {
            "message": "Cleanup completed",
            "deleted_count": deleted_count,
            "cutoff_date": cutoff_date
        }


@router.get("/export")
async def export_archive_data(
    item_type: Optional[str] = Query(None, description="내보낼 항목 유형"),
    format_type: str = Query("json", description="내보내기 형식 (json, csv)"),
    current_user: str = Depends(verify_token)
):
    """아카이브 데이터 내보내기"""
    items = list(fake_archive_db.values())

    # 유형 필터
    if item_type:
        items = [item for item in items if item["type"] == item_type]

    if format_type == "csv":
        # CSV 형식으로 변환 (간단한 구현)
        csv_data = "id,type,title,user_email,archived_date,archived_reason\n"
        for item in items:
            csv_data += f"{item['id']},{item['type']},{item['title']},{item['user_email']},{item['archived_date']},{item['archived_reason']}\n"

        logger.info(f"Archive data exported as CSV by {current_user}")

        return {
            "format": "csv",
            "data": csv_data,
            "total_items": len(items)
        }
    else:
        # JSON 형식
        logger.info(f"Archive data exported as JSON by {current_user}")

        return {
            "format": "json",
            "data": items,
            "total_items": len(items)
        }
