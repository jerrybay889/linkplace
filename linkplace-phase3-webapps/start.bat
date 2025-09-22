@echo off
chcp 65001 >nul
echo 🚀 LinkPlace Phase 3 웹 애플리케이션 시작
echo =========================================

echo 📁 현재 위치: %cd%

echo.
echo 🔧 관리자 대시보드 설정 중...
cd admin-dashboard
if not exist "node_modules" (
    echo 📦 의존성 설치 중...
    call npm install
)

echo 🌟 관리자 대시보드 실행 중 (포트: 3000)
start "관리자 대시보드" cmd /k "npm run dev"

cd ../merchant-portal
echo.
echo 🔧 광고주 포털 설정 중...
if not exist "node_modules" (
    echo 📦 의존성 설치 중...
    call npm install
)

echo 🌟 광고주 포털 실행 중 (포트: 3001)  
start "광고주 포털" cmd /k "npm run dev"

cd ..

echo.
echo ✅ 애플리케이션 실행 완료!
echo =========================================
echo 🔗 관리자 대시보드: http://localhost:3000
echo 🔗 광고주 포털: http://localhost:3001
echo.
echo 각 창을 닫으면 해당 서버가 종료됩니다
pause
