#!/bin/bash

# LinkPlace Phase 3 웹 애플리케이션 실행 스크립트
echo "🚀 LinkPlace Phase 3 웹 애플리케이션 시작"
echo "========================================="

# 현재 디렉토리 확인
CURRENT_DIR=$(pwd)
echo "📁 현재 위치: $CURRENT_DIR"

# 관리자 대시보드 실행
echo ""
echo "🔧 관리자 대시보드 설정 중..."
cd admin-dashboard
if [ ! -d "node_modules" ]; then
    echo "📦 의존성 설치 중..."
    npm install
fi

echo "🌟 관리자 대시보드 실행 중 (포트: 3000)"
npm run dev &
ADMIN_PID=$!

# 광고주 포털 실행
cd ../merchant-portal
echo ""
echo "🔧 광고주 포털 설정 중..."
if [ ! -d "node_modules" ]; then
    echo "📦 의존성 설치 중..."
    npm install
fi

echo "🌟 광고주 포털 실행 중 (포트: 3001)"
npm run dev &
MERCHANT_PID=$!

cd ..

echo ""
echo "✅ 애플리케이션 실행 완료!"
echo "========================================="
echo "🔗 관리자 대시보드: http://localhost:3000"
echo "🔗 광고주 포털: http://localhost:3001"
echo ""
echo "종료하려면 Ctrl+C를 누르세요"

# PID 저장
echo $ADMIN_PID > admin.pid
echo $MERCHANT_PID > merchant.pid

# 종료 신호 처리
cleanup() {
    echo ""
    echo "🛑 애플리케이션 종료 중..."
    kill $ADMIN_PID $MERCHANT_PID 2>/dev/null
    rm -f admin.pid merchant.pid
    echo "✅ 정상 종료되었습니다"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 대기
wait
