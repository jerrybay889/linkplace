# LinkPlace Phase 1.5 Backend API

매장 리뷰 및 포인트 시스템을 위한 FastAPI 기반 백엔드 서비스입니다.

## 🚀 주요 기능

### Phase 1.5 새로운 기능
- **포인트 시스템**: 리뷰 작성, 캠페인 참여로 포인트 적립 및 사용
- **캠페인 시스템**: 다양한 이벤트 및 프로모션 관리
- **아카이브 시스템**: 삭제된 데이터의 안전한 보관 및 복원
- **고급 리뷰 기능**: 사진 업로드, 좋아요, 도움됨 표시

### 기존 기능 (Phase 1)
- **사용자 인증**: JWT 토큰 기반 로그인/회원가입
- **매장 관리**: 매장 등록, 조회, 수정, 삭제
- **리뷰 시스템**: 매장 리뷰 작성 및 관리
- **위치 기반 검색**: 현재 위치 기반 매장 검색

## 📋 API 엔드포인트

### 🔐 인증 (Authentication)
- `POST /api/v1/auth/register` - 회원가입
- `POST /api/v1/auth/login` - 로그인
- `GET /api/v1/auth/me` - 현재 사용자 정보
- `POST /api/v1/auth/logout` - 로그아웃
- `POST /api/v1/auth/refresh` - 토큰 갱신

### 🏪 매장 (Stores)
- `GET /api/v1/stores/` - 매장 목록 조회 (필터링, 페이징 지원)
- `GET /api/v1/stores/{store_id}` - 특정 매장 조회
- `POST /api/v1/stores/` - 새 매장 등록 🔒
- `PUT /api/v1/stores/{store_id}` - 매장 정보 수정 🔒
- `DELETE /api/v1/stores/{store_id}` - 매장 삭제 🔒
- `GET /api/v1/stores/categories/` - 매장 카테고리 목록
- `GET /api/v1/stores/{store_id}/nearby` - 주변 매장 조회

### 📝 리뷰 (Reviews)
- `GET /api/v1/reviews/` - 리뷰 목록 조회
- `GET /api/v1/reviews/{review_id}` - 특정 리뷰 조회
- `POST /api/v1/reviews/` - 새 리뷰 작성 🔒
- `PUT /api/v1/reviews/{review_id}` - 리뷰 수정 🔒
- `DELETE /api/v1/reviews/{review_id}` - 리뷰 삭제 🔒
- `POST /api/v1/reviews/{review_id}/like` - 리뷰 좋아요 🔒
- `POST /api/v1/reviews/{review_id}/helpful` - 리뷰 도움됨 표시 🔒
- `POST /api/v1/reviews/{review_id}/images` - 리뷰 이미지 업로드 🔒
- `GET /api/v1/reviews/stats/store/{store_id}` - 매장 리뷰 통계

### 💰 포인트 (Points) ⭐ New in Phase 1.5
- `GET /api/v1/points/balance` - 포인트 잔액 조회 🔒
- `GET /api/v1/points/history` - 포인트 거래 내역 🔒
- `POST /api/v1/points/earn` - 포인트 적립 🔒
- `POST /api/v1/points/use` - 포인트 사용 🔒
- `POST /api/v1/points/approve/{transaction_id}` - 포인트 거래 승인 🔒👑
- `POST /api/v1/points/reject/{transaction_id}` - 포인트 거래 거부 🔒👑
- `GET /api/v1/points/expiring` - 만료 예정 포인트 조회 🔒
- `GET /api/v1/points/stats` - 포인트 통계 🔒

### 🎯 캠페인 (Campaigns) ⭐ New in Phase 1.5
- `GET /api/v1/campaigns/` - 캠페인 목록 조회
- `GET /api/v1/campaigns/{campaign_id}` - 특정 캠페인 조회
- `POST /api/v1/campaigns/` - 새 캠페인 생성 🔒👑
- `PUT /api/v1/campaigns/{campaign_id}` - 캠페인 수정 🔒👑
- `DELETE /api/v1/campaigns/{campaign_id}` - 캠페인 삭제 🔒👑
- `POST /api/v1/campaigns/{campaign_id}/participate` - 캠페인 참여 🔒
- `GET /api/v1/campaigns/{campaign_id}/participants` - 참여자 목록 🔒👑
- `POST /api/v1/campaigns/participations/{participation_id}/approve` - 참여 승인 🔒👑
- `POST /api/v1/campaigns/participations/{participation_id}/reject` - 참여 거부 🔒👑
- `POST /api/v1/campaigns/participations/{participation_id}/claim-reward` - 보상 수령 🔒
- `GET /api/v1/campaigns/my-participations` - 내 참여 내역 🔒

### 📦 아카이브 (Archive) ⭐ New in Phase 1.5
- `GET /api/v1/archive/` - 아카이브 항목 목록 🔒👑
- `GET /api/v1/archive/{archive_id}` - 특정 아카이브 항목 조회 🔒👑
- `POST /api/v1/archive/reviews/{review_id}` - 리뷰 아카이브 🔒👑
- `POST /api/v1/archive/campaigns/{campaign_id}` - 캠페인 아카이브 🔒👑
- `POST /api/v1/archive/stores/{store_id}` - 매장 아카이브 🔒👑
- `POST /api/v1/archive/{archive_id}/restore` - 아카이브 항목 복원 🔒👑
- `DELETE /api/v1/archive/{archive_id}` - 아카이브 항목 영구 삭제 🔒👑
- `GET /api/v1/archive/stats/summary` - 아카이브 통계 🔒👑
- `POST /api/v1/archive/cleanup` - 오래된 아카이브 정리 🔒👑
- `GET /api/v1/archive/export` - 아카이브 데이터 내보내기 🔒👑

**범례:**
- 🔒 인증 필요
- 👑 관리자 권한 필요
- ⭐ Phase 1.5 신규 기능

## 🛠️ 기술 스택

- **프레임워크**: FastAPI 0.104.1
- **Python**: 3.11+
- **인증**: JWT (JSON Web Tokens)
- **비밀번호 해싱**: bcrypt
- **데이터 검증**: Pydantic
- **문서화**: Swagger UI (자동 생성)
- **컨테이너화**: Docker & Docker Compose

## 📦 설치 및 실행

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd linkplace-phase1.5-backend
```

### 2. 환경 설정
```bash
# 환경 변수 파일 복사
cp .env.example .env

# 필요에 따라 .env 파일 수정
nano .env
```

### 3. Docker를 사용한 실행 (권장)
```bash
# Docker Compose로 전체 서비스 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f backend
```

### 4. 로컬 개발 환경 실행
```bash
# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

## 📚 API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 설정 항목

### 환경 변수
주요 환경 변수들은 `.env.example` 파일을 참고하세요:

- `JWT_SECRET_KEY`: JWT 토큰 서명용 비밀키
- `JWT_EXPIRE_MINUTES`: 토큰 만료 시간 (기본: 30분)
- `CORS_ORIGINS`: CORS 허용 도메인
- `UPLOAD_DIR`: 파일 업로드 디렉토리
- `MAX_FILE_SIZE`: 최대 파일 크기 (기본: 10MB)

### 기본 사용자 계정
개발용 기본 관리자 계정:
- 이메일: `admin@linkplace.com`
- 비밀번호: `secret`

## 🏗️ 프로젝트 구조

```
linkplace-phase1.5-backend/
├── main.py                    # FastAPI 애플리케이션 진입점
├── requirements.txt           # Python 패키지 의존성
├── .env.example              # 환경 변수 템플릿
├── Dockerfile                # Docker 이미지 정의
├── docker-compose.yml        # Docker Compose 설정
├── .gitignore               # Git 제외 파일 목록
├── README.md                # 프로젝트 문서 (이 파일)
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py           # 인증 API
│   │           ├── stores.py         # 매장 API
│   │           ├── reviews.py        # 리뷰 API
│   │           ├── points.py         # 포인트 API ⭐
│   │           ├── campaigns.py      # 캠페인 API ⭐
│   │           └── archive.py        # 아카이브 API ⭐
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py                   # 인증 스키마
│   │   ├── stores.py                 # 매장 스키마
│   │   ├── reviews.py                # 리뷰 스키마
│   │   ├── points.py                 # 포인트 스키마 ⭐
│   │   └── campaigns.py              # 캠페인 스키마 ⭐
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── middleware.py             # 커스텀 미들웨어
│   ├── core/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── tests/
│   └── __init__.py
└── docs/
```

## 🔄 Phase 1.5 변경사항

### 새로 추가된 기능
1. **포인트 시스템**
   - 리뷰 작성, 캠페인 참여로 포인트 적립
   - 쿠폰 구매 등에 포인트 사용
   - 포인트 만료 관리
   - 관리자 승인/거부 시스템

2. **캠페인 시스템**
   - 다양한 유형의 캠페인 생성 및 관리
   - 사용자 참여 및 보상 시스템
   - 캠페인 조건 설정 및 검증
   - 참여 내역 관리

3. **아카이브 시스템**
   - 삭제된 데이터의 안전한 보관
   - 아카이브 항목 복원 기능
   - 오래된 아카이브 자동 정리
   - 데이터 내보내기 기능

4. **리뷰 시스템 개선**
   - 사진 업로드 기능
   - 좋아요 및 도움됨 표시
   - 매장별 리뷰 통계

### 개선된 기능
- 향상된 에러 처리
- 보안 헤더 추가
- 상세한 로깅
- API 문서 개선

## 🧪 테스트

```bash
# 테스트 실행 (향후 구현 예정)
pytest

# 커버리지 포함 테스트
pytest --cov=app tests/
```

## 🚀 배포

### Docker를 사용한 프로덕션 배포
```bash
# 프로덕션 환경 변수 설정
cp .env.example .env.production
# .env.production 파일 수정

# 프로덕션 이미지 빌드
docker build -t linkplace-backend:latest .

# 프로덕션 실행
docker run -d --name linkplace-backend   --env-file .env.production   -p 8000:8000   linkplace-backend:latest
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.

## 📞 연락처

프로젝트 관련 문의: [your-email@example.com]

---

**LinkPlace Phase 1.5 Backend** - 매장 리뷰 및 포인트 시스템을 위한 완전한 백엔드 솔루션
