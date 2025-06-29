# TicketLink Launcher

티켓링크 웹사이트를 자동화하여 티켓 예매를 도와주는 Python 매크로 프로그램입니다.

## 🚀 주요 기능

- 티켓링크 웹사이트 자동 접속
- 로그인 자동화 (PAYCO 로그인 지원)
- **기존 크롬 세션 활용 (권장)**
- 티켓 검색 및 예매 시도
- 예매 성공 시 알림 기능

## 📋 설치 방법

1. 저장소를 클론합니다:
```bash
git clone https://github.com/yourusername/TicketLinkLauncher.git
cd TicketLinkLauncher
```

2. 가상환경을 생성하고 활성화합니다:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

## 🔧 사용 방법

### 방법 1: 기존 크롬 세션 활용 (권장)

PAYCO 로그인의 복잡한 인증 과정을 우회하기 위해 이미 로그인된 크롬 창을 활용합니다.

1. **크롬을 디버깅 모드로 시작:**
   ```bash
   # Windows
   start_chrome_debug.bat
   
   # 또는 수동으로:
   chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\temp\chrome_debug
   ```

2. **새로 열린 크롬 창에서 티켓링크에 로그인**

3. **매크로 실행:**
   ```bash
   python main.py
   # 선택: 4 (기존 크롬 세션 활용)
   ```

### 방법 2: 자동 로그인

1. `.env` 파일을 생성하고 필요한 설정을 입력합니다:
```
TICKETLINK_ID=your_id
TICKETLINK_PASSWORD=your_password
TICKETLINK_BIRTHDAY=19820124
```

2. 프로그램을 실행합니다:
```bash
python main.py
# 선택: 1 (로그인 테스트만) 또는 2 (전체 예매 테스트)
```

## 🎯 실행 모드

프로그램 실행 시 다음 모드 중 선택할 수 있습니다:

1. **로그인 테스트만** - 로그인 기능만 테스트
2. **전체 예매 테스트** - 로그인부터 예매까지 전체 과정 테스트
3. **직접 PAYCO 로그인 테스트** - PAYCO 로그인만 테스트
4. **기존 크롬 세션 활용 (권장)** - 이미 로그인된 크롬 창 활용

## 🔍 문제 해결

### PAYCO 로그인 문제
- PAYCO는 불규칙적으로 생년월일 인증, 문자 인증 등을 요구합니다
- **기존 크롬 세션 활용 방법을 권장합니다**

### Chrome 연결 오류
- 크롬이 디버깅 모드로 실행되지 않은 경우 발생
- `start_chrome_debug.bat`을 실행하여 크롬을 재시작하세요

### Python 버전 문제
- Python 3.13에서는 `undetected_chromedriver` 호환성 문제가 있을 수 있습니다
- Python 3.12 이하 버전 사용을 권장합니다

## ⚠️ 주의사항

- 이 프로그램은 교육 목적으로 제작되었습니다
- 실제 사용 시에는 해당 웹사이트의 이용약관을 준수해주세요
- 과도한 요청으로 인한 서버 부하를 방지하기 위해 적절한 딜레이를 설정해주세요
- 매크로 감지 시스템이 있을 수 있으니 주의해서 사용하세요

## 📁 파일 구조

```
TicketLinkLauncher/
├── main.py                 # 메인 실행 파일
├── ticketlink_bot.py       # 티켓링크 봇 클래스
├── use_existing_chrome.py  # 기존 크롬 세션 활용 스크립트
├── start_chrome_debug.bat  # 크롬 디버깅 모드 시작 배치 파일
├── test_payco_login.py     # PAYCO 로그인 테스트
├── requirements.txt        # 필요한 패키지 목록
├── .env                    # 환경 변수 (사용자가 생성)
├── env.example            # 환경 변수 예시
└── utils/
    ├── __init__.py
    └── logger.py          # 로깅 유틸리티
```

## 🛠️ 개발 환경

- Python 3.8+
- Chrome 브라우저
- Selenium WebDriver
- undetected-chromedriver (선택사항)

## 📄 라이선스

MIT License

## 🤝 기여

버그 리포트나 기능 제안은 이슈를 통해 해주세요. 