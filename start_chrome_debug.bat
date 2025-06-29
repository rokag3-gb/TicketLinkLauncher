@echo off
echo 🚀 Chrome 디버깅 모드로 시작합니다...
echo.

REM 기존 크롬 프로세스 종료
taskkill /f /im chrome.exe 2>nul
timeout /t 2 /nobreak >nul

REM Chrome 디버깅 모드로 시작
echo Chrome을 디버깅 모드로 시작합니다...
echo 포트: 9222
echo 사용자 데이터 디렉토리: C:\temp\chrome_debug
echo.

REM 사용자 데이터 디렉토리 생성
if not exist "C:\temp\chrome_debug" mkdir "C:\temp\chrome_debug"

REM Chrome 시작
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir=C:\temp\chrome_debug

echo.
echo ✅ Chrome이 디버깅 모드로 시작되었습니다.
echo 📝 이제 Chrome에서 티켓링크에 로그인하세요.
echo 🔗 로그인 완료 후 use_existing_chrome.py를 실행하세요.
echo.
pause 