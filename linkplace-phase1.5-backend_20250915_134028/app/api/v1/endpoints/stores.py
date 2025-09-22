"""
매장 관련 API 엔드포인트
"""

from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
import logging
from datetime import datetime

from app.schemas.stores import StoreCreate, StoreUpdate, StoreResponse, StoreList
from app.api.v1.endpoints.auth import verify_token

router = APIRouter()
logger = logging.getLogger(__name__)

# 임시 매장 데이터
fake_stores_db = {
    1: {
        "id": 1,
        "name": "강남 카페",
        "category": "카페",
        "address": "서울시 강남구 강남대로 123",
        "phone": "02-1234-5678",
        "description": "강남의 아늑한 카페입니다.",
        "latitude": 37.4979,
        "longitude": 127.0276,
        "business_hours": "09:00-22:00",
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "rating": 4.5,
        "review_count": 42
    },
    2: {
        "id": 2,
        "name": "홍대 펍",
        "category": "주점",
        "address": "서울시 마포구 홍익로 456",
        "phone": "02-2345-6789",
        "description": "홍대의 핫한 펍입니다.",
        "latitude": 37.5563,
        "longitude": 126.9236,
        "business_hours": "17:00-02:00",
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "rating": 4.2,
        "review_count": 28
    }
}


@router.get("/", response_model=StoreList)
async def get_stores(
    category: Optional[str] = Query(None, description="매장 카테고리 필터"),
    search: Optional[str] = Query(None, description="매장명 검색"),
    latitude: Optional[float] = Query(None, description="현재 위도"),
    longitude: Optional[float] = Query(None, description="현재 경도"),
    radius: Optional[float] = Query(10.0, description="검색 반경 (km)"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기")
):
    """매장 목록 조회"""
    stores = list(fake_stores_db.values())

    # 카테고리 필터
    if category:
        stores = [store for store in stores if store["category"] == category]

    # 검색 필터
    if search:
        search_lower = search.lower()
        stores = [store for store in stores if search_lower in store["name"].lower()]

    # 활성 매장만 필터
    stores = [store for store in stores if store["is_active"]]

    # 거리 계산 (간단한 구현)
    if latitude is not None and longitude is not None:
        def calculate_distance(lat1, lon1, lat2, lon2):
            # 간단한 거리 계산 (실제로는 haversine formula 사용)
            return ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5 * 111  # 대략적인 km 변환

        stores_with_distance = []
        for store in stores:
            distance = calculate_distance(
                latitude, longitude, 
                store["latitude"], store["longitude"]
            )
            if distance <= radius:
                store["distance"] = round(distance, 2)
                stores_with_distance.append(store)

        # 거리순 정렬
        stores = sorted(stores_with_distance, key=lambda x: x["distance"])

    # 페이지네이션
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    paginated_stores = stores[start_idx:end_idx]

    return StoreList(
        stores=[StoreResponse(**store) for store in paginated_stores],
        total=len(stores),
        page=page,
        size=size,
        pages=(len(stores) + size - 1) // size
    )


@router.get("/{store_id}", response_model=StoreResponse)
async def get_store(store_id: int):
    """특정 매장 조회"""
    store = fake_stores_db.get(store_id)

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )

    if not store["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not available"
        )

    return StoreResponse(**store)


@router.post("/", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(
    store_data: StoreCreate,
    current_user: str = Depends(verify_token)
):
    """새 매장 등록"""
    # 새 매장 ID 생성
    new_id = max(fake_stores_db.keys()) + 1 if fake_stores_db else 1

    # 현재 시간
    now = datetime.now().isoformat()

    # 새 매장 데이터
    new_store = {
        "id": new_id,
        **store_data.dict(),
        "is_active": True,
        "created_at": now,
        "updated_at": now,
        "rating": 0.0,
        "review_count": 0
    }

    fake_stores_db[new_id] = new_store

    logger.info(f"Store created: {new_store['name']} by {current_user}")

    return StoreResponse(**new_store)


@router.put("/{store_id}", response_model=StoreResponse)
async def update_store(
    store_id: int,
    store_data: StoreUpdate,
    current_user: str = Depends(verify_token)
):
    """매장 정보 수정"""
    store = fake_stores_db.get(store_id)

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )

    # 업데이트할 데이터만 적용
    update_data = store_data.dict(exclude_unset=True)

    if update_data:
        store.update(update_data)
        store["updated_at"] = datetime.now().isoformat()

        logger.info(f"Store updated: {store_id} by {current_user}")

    return StoreResponse(**store)


@router.delete("/{store_id}")
async def delete_store(
    store_id: int,
    current_user: str = Depends(verify_token)
):
    """매장 삭제 (비활성화)"""
    store = fake_stores_db.get(store_id)

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )

    # 실제로는 삭제하지 않고 비활성화
    store["is_active"] = False
    store["updated_at"] = datetime.now().isoformat()

    logger.info(f"Store deactivated: {store_id} by {current_user}")

    return {"message": "Store deleted successfully"}


@router.get("/categories/", response_model=List[str])
async def get_categories():
    """매장 카테고리 목록"""
    categories = set()
    for store in fake_stores_db.values():
        if store["is_active"]:
            categories.add(store["category"])

    return sorted(list(categories))


@router.get("/{store_id}/nearby", response_model=List[StoreResponse])
async def get_nearby_stores(
    store_id: int,
    radius: float = Query(5.0, description="검색 반경 (km)"),
    limit: int = Query(10, ge=1, le=50, description="최대 결과 수")
):
    """주변 매장 조회"""
    target_store = fake_stores_db.get(store_id)

    if not target_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )

    def calculate_distance(lat1, lon1, lat2, lon2):
        return ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5 * 111

    nearby_stores = []
    target_lat = target_store["latitude"]
    target_lon = target_store["longitude"]

    for store in fake_stores_db.values():
        if store["id"] != store_id and store["is_active"]:
            distance = calculate_distance(
                target_lat, target_lon,
                store["latitude"], store["longitude"]
            )

            if distance <= radius:
                store_copy = store.copy()
                store_copy["distance"] = round(distance, 2)
                nearby_stores.append(store_copy)

    # 거리순 정렬 및 제한
    nearby_stores.sort(key=lambda x: x["distance"])
    nearby_stores = nearby_stores[:limit]

    return [StoreResponse(**store) for store in nearby_stores]
