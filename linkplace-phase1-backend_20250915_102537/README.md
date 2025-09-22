# LinkPlace Backend - Phase 1

> 🚀 **Phase 1 백엔드 개발 완료** - 사용자 인증, 소셜 로그인, 및 핵심 모델 구조

LinkPlace 플랫폼의 FastAPI 기반 백엔드 서버입니다. JWT 인증, 소셜 로그인(네이버, 구글, 카카오), 그리고 확장 가능한 아키텍처를 제공합니다.

## ✨ 주요 기능

### 🔐 인증 시스템
- **JWT 기반 인증** - Access Token + Refresh Token
- **소셜 로그인** - 네이버, 구글, 카카오 OAuth2 지원
- **보안 강화** - 패스워드 해싱, 토큰 만료 관리

### 🗄️ 데이터베이스 모델
- **User** - 사용자 관리 (고객/상점주/관리자)
- **Merchant** - 사업자 등록 및 관리
- **Store** - 매장 정보 및 위치 관리
- **Campaign** - 마케팅 캠페인 시스템
- **Review** - 리뷰 및 평점 시스템
- **PointTransaction** - 포인트 적립/사용 내역

### 🛠️ 기술 스택
- **FastAPI** - 고성능 웹 프레임워크
- **SQLAlchemy 2.0** - 비동기 ORM
- **PostgreSQL** - 메인 데이터베이스
- **Redis** - 캐싱 및 세션 관리
- **Celery** - 백그라운드 작업 처리
- **Pydantic** - 데이터 검증 및 직렬화

## 📋 시스템 요구사항

### 소프트웨어 요구사항
- **Python 3.9+**
- **PostgreSQL 13+**
- **Redis 6+**

### 권장 환경
- **운영체제**: Ubuntu 20.04+ / CentOS 7+ / macOS 10.15+
- **메모리**: 최소 2GB, 권장 4GB+
- **디스크**: 최소 5GB 여유 공간

## 🚀 설치 및 실행

### 1. 프로젝트 클론 및 가상환경 설정

```bash
# 프로젝트 디렉토리로 이동
cd linkplace-phase1-backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 2. 의존성 설치

```bash
# 프로덕션 의존성 설치
pip install -r requirements.txt

# 개발 의존성 추가 설치 (개발 환경인 경우)
pip install -r requirements-dev.txt
```

### 3. 데이터베이스 설정

#### PostgreSQL 설치 및 설정

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql-server postgresql-contrib
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql

# macOS (Homebrew)
brew install postgresql
brew services start postgresql
```

#### 데이터베이스 생성

```bash
# PostgreSQL에 접속
sudo -u postgres psql

# 데이터베이스 및 사용자 생성
CREATE DATABASE linkplace;
CREATE USER linkplace WITH ENCRYPTED PASSWORD 'linkplace123';
GRANT ALL PRIVILEGES ON DATABASE linkplace TO linkplace;

# 종료
\q
```

### 4. Redis 설치 및 실행

```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

# CentOS/RHEL
sudo yum install redis
sudo systemctl start redis
sudo systemctl enable redis

# macOS (Homebrew)
brew install redis
brew services start redis

# Redis 연결 테스트
redis-cli ping
# 응답: PONG
```

### 5. 환경 변수 설정

```bash
# .env.example을 복사하여 .env 생성
cp .env.example .env

# .env 파일 편집
nano .env
```

#### 필수 환경 변수 설정

```env
# 데이터베이스 설정 (실제 값으로 변경)
DATABASE_URL=postgresql+asyncpg://linkplace:linkplace123@localhost:5432/linkplace
DATABASE_URL_SYNC=postgresql://linkplace:linkplace123@localhost:5432/linkplace

# JWT 보안키 (운영 환경에서 반드시 변경)
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# 소셜 로그인 설정 (각 플랫폼에서 발급받은 키로 변경)
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
KAKAO_CLIENT_ID=your_kakao_client_id
KAKAO_CLIENT_SECRET=your_kakao_client_secret
```

### 6. 데이터베이스 마이그레이션

```bash
# Alembic 초기화 (이미 설정되어 있음)
# alembic init alembic

# 마이그레이션 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 실행
alembic upgrade head
```

### 7. 서버 실행

```bash
# 개발 서버 실행 (자동 리로드 포함)
python main.py

# 또는 uvicorn 직접 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 프로덕션 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🌐 API 엔드포인트

### 기본 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 루트 엔드포인트 |
| GET | `/health` | 헬스 체크 |
| GET | `/info` | 애플리케이션 정보 |
| GET | `/docs` | API 문서 (Swagger UI) |
| GET | `/redoc` | API 문서 (ReDoc) |

### API 접근

```bash
# 서버 상태 확인
curl http://localhost:8000/health

# API 문서 접근
# 브라우저에서 http://localhost:8000/docs 열기
```

## 📁 프로젝트 구조

```
linkplace-phase1-backend/
├── app/                          # 메인 애플리케이션
│   ├── __init__.py
│   ├── core/                     # 핵심 구성 요소
│   │   ├── __init__.py
│   │   ├── config.py             # 설정 관리
│   │   ├── database.py           # 데이터베이스 연결
│   │   └── auth.py               # 인증 의존성
│   ├── models/                   # SQLAlchemy 모델
│   │   ├── __init__.py
│   │   ├── user.py               # 사용자 모델
│   │   ├── merchant.py           # 상점주 모델
│   │   ├── store.py              # 매장 모델
│   │   ├── campaign.py           # 캠페인 모델
│   │   ├── review.py             # 리뷰 모델
│   │   └── point_transaction.py  # 포인트 거래 모델
│   ├── schemas/                  # Pydantic 스키마
│   │   ├── __init__.py
│   │   ├── user.py               # 사용자 스키마
│   │   └── auth.py               # 인증 스키마
│   ├── services/                 # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── user_service.py       # 사용자 서비스
│   │   └── social_auth.py        # 소셜 인증 서비스
│   ├── utils/                    # 유틸리티
│   │   ├── __init__.py
│   │   └── jwt.py                # JWT 유틸리티
│   └── api/                      # API 엔드포인트
│       └── v1/
│           └── endpoints/
├── alembic/                      # 데이터베이스 마이그레이션
├── main.py                       # FastAPI 애플리케이션
├── requirements.txt              # 프로덕션 의존성
├── requirements-dev.txt          # 개발 의존성
├── .env.example                  # 환경 변수 예시
├── .env                          # 환경 변수 (실제)
├── alembic.ini                   # Alembic 설정
└── README.md                     # 이 파일
```

## 🔧 개발 가이드

### 코드 스타일

```bash
# 코드 포매팅
black app/ main.py

# Import 정렬
isort app/ main.py

# 린팅
flake8 app/ main.py

# 타입 체크
mypy app/
```

### 테스트 실행

```bash
# 테스트 실행
pytest

# 커버리지 포함 테스트
pytest --cov=app tests/

# 특정 테스트 파일 실행
pytest tests/test_auth.py
```

### 새로운 모델 추가

1. `app/models/`에 새 모델 파일 생성
2. `app/models/__init__.py`에 import 추가
3. Alembic 마이그레이션 생성 및 적용
4. 해당 Pydantic 스키마 작성
5. 서비스 로직 구현

### 새로운 API 엔드포인트 추가

1. `app/api/v1/endpoints/`에 라우터 파일 생성
2. `main.py`에 라우터 등록
3. 필요한 스키마 및 서비스 구현

## 🐳 Docker 배포 (향후 지원 예정)

```dockerfile
# Dockerfile 예시
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔍 문제 해결

### 일반적인 문제들

#### 1. 데이터베이스 연결 실패
```bash
# PostgreSQL 서비스 상태 확인
sudo systemctl status postgresql

# PostgreSQL 연결 테스트
psql -h localhost -U linkplace -d linkplace
```

#### 2. Redis 연결 실패
```bash
# Redis 서비스 상태 확인
sudo systemctl status redis

# Redis 연결 테스트
redis-cli ping
```

#### 3. 의존성 설치 실패
```bash
# pip 업그레이드
pip install --upgrade pip

# 캐시 클리어 후 재설치
pip cache purge
pip install -r requirements.txt
```

#### 4. 포트 충돌
```bash
# 포트 8000 사용 중인 프로세스 확인
lsof -i :8000

# 다른 포트로 실행
uvicorn main:app --port 8001
```

## 📚 추가 리소스

### 문서 및 학습 자료
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/en/20/)
- [Pydantic 문서](https://pydantic-docs.helpmanual.io/)
- [Alembic 문서](https://alembic.sqlalchemy.org/)

### 소셜 로그인 설정 가이드
- [네이버 로그인 API](https://developers.naver.com/docs/login/api/)
- [구글 OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [카카오 로그인](https://developers.kakao.com/docs/latest/ko/kakaologin/common)

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원

문제가 발생하거나 질문이 있으시면:

- 📧 이메일: dev@linkplace.co.kr
- 🐛 이슈 트래커: [GitHub Issues](https://github.com/linkplace/backend/issues)
- 📖 Wiki: [프로젝트 Wiki](https://github.com/linkplace/backend/wiki)

---

**LinkPlace Team** ❤️ *2024년도 개발*
