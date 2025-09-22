"""
리뷰 관련 API 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Query, Depends, status, UploadFile, File, Form
from typing import List, Optional
import logging
from datetime import datetime
import uuid
import os

from app.schemas.reviews import ReviewCreate, ReviewUpdate, ReviewResponse, ReviewList
from app.api.v1.endpoints.auth import verify_token

router = APIRouter()
logger = logging.getLogger(__name__)

# 임시 리뷰 데이터
fake_reviews_db = {
    1: {
        "id": 1,
        "store_id": 1,
        "user_email": "user1@example.com",
        "rating": 5,
        "title": "정말 좋은 카페에요!",
        "content": "분위기도 좋고 커피도 맛있어요. 직원분들도 친절하시고 다시 오고 싶은 곳입니다.",
        "images": ["/uploads/review1_1.jpg", "/uploads/review1_2.jpg"],
        "is_anonymous": False,
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-01-15T10:30:00",
        "likes": 12,
        "helpful_count": 8
    },
    2: {
        "id": 2,
        "store_id": 1,
        "user_email": "user2@example.com",
        "rating": 4,
        "title": "괜찮은 분위기",
        "content": "커피 맛은 보통이지만 분위기가 좋아서 공부하기 좋습니다.",
        "images": [],
        "is_anonymous": True,
        "created_at": "2024-01-20T14:15:00",
        "updated_at": "2024-01-20T14:15:00",
        "likes": 5,
        "helpful_count": 3
    }
}


@router.get("/", response_model=ReviewList)
async def get_reviews(
    store_id: Optional[int] = Query(None, description="매장 ID로 필터"),
    user_email: Optional[str] = Query(None, description="사용자 이메일로 필터"),
    rating_min: Optional[int] = Query(None, ge=1, le=5, description="최소 평점"),
    rating_max: Optional[int] = Query(None, ge=1, le=5, description="최대 평점"),
    sort_by: str = Query("created_at", description="정렬 기준 (created_at, rating, likes)"),
    sort_order: str = Query("desc", description="정렬 순서 (asc, desc)"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기")
):
    """리뷰 목록 조회"""
    reviews = list(fake_reviews_db.values())

    # 필터 적용
    if store_id:
        reviews = [r for r in reviews if r["store_id"] == store_id]

    if user_email:
        reviews = [r for r in reviews if r["user_email"] == user_email]

    if rating_min:
        reviews = [r for r in reviews if r["rating"] >= rating_min]

    if rating_max:
        reviews = [r for r in reviews if r["rating"] <= rating_max]

    # 정렬
    reverse_order = sort_order == "desc"
    if sort_by == "created_at":
        reviews.sort(key=lambda x: x["created_at"], reverse=reverse_order)
    elif sort_by == "rating":
        reviews.sort(key=lambda x: x["rating"], reverse=reverse_order)
    elif sort_by == "likes":
        reviews.sort(key=lambda x: x["likes"], reverse=reverse_order)

    # 페이지네이션
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    paginated_reviews = reviews[start_idx:end_idx]

    return ReviewList(
        reviews=[ReviewResponse(**review) for review in paginated_reviews],
        total=len(reviews),
        page=page,
        size=size,
        pages=(len(reviews) + size - 1) // size
    )


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int):
    """특정 리뷰 조회"""
    review = fake_reviews_db.get(review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    return ReviewResponse(**review)


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: ReviewCreate,
    current_user: str = Depends(verify_token)
):
    """새 리뷰 작성"""
    # 새 리뷰 ID 생성
    new_id = max(fake_reviews_db.keys()) + 1 if fake_reviews_db else 1

    # 현재 시간
    now = datetime.now().isoformat()

    # 새 리뷰 데이터
    new_review = {
        "id": new_id,
        "user_email": current_user,
        **review_data.dict(),
        "created_at": now,
        "updated_at": now,
        "likes": 0,
        "helpful_count": 0
    }

    fake_reviews_db[new_id] = new_review

    logger.info(f"Review created: {new_id} for store {review_data.store_id} by {current_user}")

    return ReviewResponse(**new_review)


@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    current_user: str = Depends(verify_token)
):
    """리뷰 수정"""
    review = fake_reviews_db.get(review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    # 작성자만 수정 가능
    if review["user_email"] != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    # 업데이트할 데이터만 적용
    update_data = review_data.dict(exclude_unset=True)

    if update_data:
        review.update(update_data)
        review["updated_at"] = datetime.now().isoformat()

        logger.info(f"Review updated: {review_id} by {current_user}")

    return ReviewResponse(**review)


@router.delete("/{review_id}")
async def delete_review(
    review_id: int,
    current_user: str = Depends(verify_token)
):
    """리뷰 삭제"""
    review = fake_reviews_db.get(review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    # 작성자만 삭제 가능
    if review["user_email"] != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    del fake_reviews_db[review_id]

    logger.info(f"Review deleted: {review_id} by {current_user}")

    return {"message": "Review deleted successfully"}


@router.post("/{review_id}/like")
async def like_review(
    review_id: int,
    current_user: str = Depends(verify_token)
):
    """리뷰 좋아요"""
    review = fake_reviews_db.get(review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    # 간단한 구현 (실제로는 좋아요 상태 관리 필요)
    review["likes"] += 1

    logger.info(f"Review liked: {review_id} by {current_user}")

    return {"message": "Review liked", "likes": review["likes"]}


@router.post("/{review_id}/helpful")
async def mark_helpful(
    review_id: int,
    current_user: str = Depends(verify_token)
):
    """리뷰 도움됨 표시"""
    review = fake_reviews_db.get(review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    # 간단한 구현 (실제로는 도움됨 상태 관리 필요)
    review["helpful_count"] += 1

    logger.info(f"Review marked helpful: {review_id} by {current_user}")

    return {"message": "Review marked as helpful", "helpful_count": review["helpful_count"]}


@router.post("/{review_id}/images")
async def upload_review_images(
    review_id: int,
    files: List[UploadFile] = File(...),
    current_user: str = Depends(verify_token)
):
    """리뷰 이미지 업로드"""
    review = fake_reviews_db.get(review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    # 작성자만 업로드 가능
    if review["user_email"] != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    # 이미지 파일 검증
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    uploaded_files = []

    # uploads 디렉토리 생성
    upload_dir = "/tmp/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    for file in files:
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type: {file.content_type}"
            )

        # 파일명 생성
        file_extension = file.filename.split(".")[-1]
        new_filename = f"review_{review_id}_{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(upload_dir, new_filename)

        # 파일 저장
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        uploaded_files.append(f"/uploads/{new_filename}")

    # 리뷰에 이미지 경로 추가
    if "images" not in review:
        review["images"] = []

    review["images"].extend(uploaded_files)
    review["updated_at"] = datetime.now().isoformat()

    logger.info(f"Images uploaded for review {review_id}: {len(uploaded_files)} files")

    return {
        "message": "Images uploaded successfully",
        "uploaded_files": uploaded_files,
        "total_images": len(review["images"])
    }


@router.get("/stats/store/{store_id}")
async def get_store_review_stats(store_id: int):
    """특정 매장의 리뷰 통계"""
    store_reviews = [r for r in fake_reviews_db.values() if r["store_id"] == store_id]

    if not store_reviews:
        return {
            "store_id": store_id,
            "total_reviews": 0,
            "average_rating": 0.0,
            "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }

    total_reviews = len(store_reviews)
    total_rating = sum(r["rating"] for r in store_reviews)
    average_rating = round(total_rating / total_reviews, 2)

    # 평점 분포
    rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for review in store_reviews:
        rating_distribution[review["rating"]] += 1

    return {
        "store_id": store_id,
        "total_reviews": total_reviews,
        "average_rating": average_rating,
        "rating_distribution": rating_distribution,
        "total_likes": sum(r["likes"] for r in store_reviews),
        "total_helpful": sum(r["helpful_count"] for r in store_reviews)
    }
