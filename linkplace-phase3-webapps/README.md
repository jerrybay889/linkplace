# LinkPlace Phase 3 - 웹 애플리케이션

LinkPlace의 Phase 3 웹 애플리케이션으로 관리자 웹 대시보드와 광고주 포털을 포함합니다.

## 🏗️ 프로젝트 구조

```
linkplace-phase3-webapps/
├── admin-dashboard/          # 관리자 웹 대시보드
│   ├── src/
│   │   ├── components/       # 공통 컴포넌트
│   │   ├── pages/           # 페이지 컴포넌트
│   │   ├── services/        # API 서비스
│   │   ├── types/           # TypeScript 타입 정의
│   │   └── utils/           # 유틸리티 함수
│   ├── package.json
│   └── vite.config.ts
├── merchant-portal/          # 광고주 포털
│   ├── src/
│   │   ├── components/       # 공통 컴포넌트
│   │   ├── pages/           # 페이지 컴포넌트
│   │   ├── services/        # API 서비스
│   │   ├── types/           # TypeScript 타입 정의
│   │   └── utils/           # 유틸리티 함수
│   ├── package.json
│   └── vite.config.ts
├── start.sh                  # Linux/Mac 실행 스크립트
├── start.bat                 # Windows 실행 스크립트
└── README.md
```

## 🚀 빠른 시작

### 사전 요구사항
- Node.js 18+ 
- npm 또는 yarn

### 자동 실행
#### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

#### Windows
```batch
start.bat
```

### 수동 실행

#### 1. 관리자 대시보드
```bash
cd admin-dashboard
npm install
npm run dev
```
접속: http://localhost:3000

#### 2. 광고주 포털
```bash
cd merchant-portal  
npm install
npm run dev
```
접속: http://localhost:3001

## 📱 애플리케이션 소개

### 🔐 관리자 웹 대시보드
**포트**: 3000  
**기능**:
- 실시간 통계 대시보드
- 사용자 관리 (가입, 등급, 상태)
- 매장 관리 (등록, 승인, 카테고리)
- 리뷰 관리 (검토, 승인, 통계)
- 캠페인 관리 (생성, 모니터링, 성과)
- 광고주 관리 (계정, 매장, 정산)
- 시스템 설정

**기술 스택**:
- React 18 + TypeScript
- Ant Design UI 라이브러리
- Recharts (차트)
- Vite 개발 도구

### 🏪 광고주 포털  
**포트**: 3001  
**기능**:
- 광고주 전용 대시보드
- 매장 관리 (등록, 수정, 현황)
- 캠페인 관리 (생성, 실행, 분석)
- 리뷰 관리 (응답, 모니터링)
- 분석 리포트 (방문자, 전환율, 수익)
- 계정 설정

**기술 스택**:
- React 18 + TypeScript
- Ant Design UI 라이브러리  
- Recharts (차트)
- Vite 개발 도구

## 🛠️ 개발

### 개발 명령어
```bash
# 개발 서버 시작
npm run dev

# 빌드
npm run build

# 빌드 미리보기
npm run preview

# 타입 체크
npm run type-check

# 린트
npm run lint
```

### 프로젝트 특징
- **TypeScript**: 타입 안전성 보장
- **모듈화 구조**: 컴포넌트와 페이지 분리
- **반응형 디자인**: 모바일/데스크톱 대응
- **실시간 차트**: 데이터 시각화
- **한국어 지원**: 완전 한국어 UI

## 📋 주요 기능

### 관리자 기능
- ✅ 통계 대시보드 (사용자, 매장, 리뷰, 수익)
- ✅ 사용자 관리 (검색, 수정, 삭제, 등급)
- ✅ 매장 관리 (승인, 카테고리, 평점)
- ✅ 리뷰 검토 및 승인
- ✅ 캠페인 모니터링
- ✅ 광고주 계정 관리
- ✅ 시스템 설정

### 광고주 기능  
- ✅ 매장별 대시보드
- ✅ 매장 등록 및 관리
- ✅ 캠페인 생성 및 관리
- ✅ 리뷰 응답 관리
- ✅ 성과 분석 리포트
- ✅ 계정 설정

## 🔧 기술적 세부사항

### 아키텍처
- **프론트엔드**: React SPA
- **상태 관리**: React Hooks + Context API
- **라우팅**: React Router v6
- **UI 프레임워크**: Ant Design v5
- **빌드 도구**: Vite
- **타입 시스템**: TypeScript

### 성능 최적화
- 코드 분할 (Code Splitting)
- 지연 로딩 (Lazy Loading)  
- 번들 최적화
- 트리 셰이킹

## 📞 지원

문의사항이나 버그 리포트는 개발팀에 연락해주세요.

---

**LinkPlace Team** © 2024
