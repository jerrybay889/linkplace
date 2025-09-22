# LinkPlace React Native App

링크플레이스는 관광객 대상 구글 리뷰 오퍼월 서비스를 제공하는 React Native 모바일 애플리케이션입니다.

## 주요 기능

- **사용자 인증**: 로그인/회원가입 기능
- **매장 검색**: 주변 매장 검색 및 위치 기반 서비스
- **리뷰 작성**: 구글 리뷰 작성 및 포인트 적립
- **포인트 관리**: 포인트 적립/사용 내역 관리
- **사용자 프로필**: 개인정보 관리 및 설정

## 기술 스택

- **Frontend**: React Native (Expo)
- **언어**: TypeScript
- **상태 관리**: Redux Toolkit
- **네비게이션**: React Navigation v6
- **UI 라이브러리**: React Native Elements
- **데이터 저장**: Redux Persist (AsyncStorage)

## 프로젝트 구조

```
src/
├── components/          # 재사용 가능한 컴포넌트
│   └── common/         # 공통 컴포넌트 (Button, Input, Card 등)
├── screens/            # 화면 컴포넌트
│   ├── auth/          # 인증 관련 화면
│   ├── home/          # 홈 화면
│   ├── search/        # 검색 화면
│   ├── review/        # 리뷰 관리 화면
│   ├── points/        # 포인트 관리 화면
│   └── profile/       # 프로필 화면
├── navigation/         # 네비게이션 설정
├── store/             # Redux 스토어
│   ├── slices/       # Redux 슬라이스
│   └── api/          # API 관련 설정
├── types/            # TypeScript 타입 정의
├── theme/            # 테마 및 스타일 설정
├── utils/            # 유틸리티 함수
├── hooks/            # 커스텀 훅
└── services/         # 외부 서비스 연동
```

## 설치 및 실행

### 필요 조건

- Node.js 16.x 이상
- npm 또는 yarn
- Expo CLI
- React Native 개발 환경

### 설치 방법

1. 프로젝트 클론
```bash
git clone <repository-url>
cd LinkPlace-ReactNative
```

2. 의존성 설치
```bash
npm install
# 또는
yarn install
```

3. 개발 서버 실행
```bash
npm start
# 또는
yarn start
```

4. 앱 실행
- iOS: `npm run ios` 또는 Expo Go 앱에서 QR 코드 스캔
- Android: `npm run android` 또는 Expo Go 앱에서 QR 코드 스캔

## 환경 변수 설정

`.env` 파일을 생성하고 다음 변수들을 설정하세요:

```
API_BASE_URL=https://your-api-server.com
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

## 빌드

### 개발 빌드
```bash
expo build:android
expo build:ios
```

### 프로덕션 빌드
```bash
expo build:android --type app-bundle
expo build:ios --type archive
```

## 배포

1. Android Play Store
2. iOS App Store

## 개발 가이드

### 코드 스타일

- ESLint와 Prettier 사용
- TypeScript strict 모드 사용
- 컴포넌트는 함수형 컴포넌트로 작성
- 상태 관리는 Redux Toolkit 사용

### 폴더 구조 규칙

- 컴포넌트는 PascalCase 사용
- 파일명은 컴포넌트명과 동일하게 설정
- 인덱스 파일을 통한 export 관리

### Git 커밋 컨벤션

- feat: 새로운 기능 추가
- fix: 버그 수정
- docs: 문서 수정
- style: 코드 스타일 변경
- refactor: 코드 리팩토링
- test: 테스트 추가/수정

## API 연동

백엔드 API 서버와의 연동을 위해 `src/services/` 폴더에 API 클라이언트를 구현하세요.

## 테스트

```bash
npm test
# 또는
yarn test
```

## 라이센스

MIT License

## 기여하기

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 문의

프로젝트 관련 문의사항이 있으시면 이슈를 생성해 주세요.
