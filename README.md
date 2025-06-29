# TicketLink Launcher

티켓링크 웹사이트를 자동화하여 티켓 예매를 도와주는 Python 매크로 프로그램입니다.

## 🚀 주요 기능

- 티켓링크 웹사이트 자동 접속
- 로그인 자동화 (PAYCO 로그인 지원)
- **기존 크롬 세션 활용 (권장)**
- **PyAutoGUI 기반 전체 예매 자동화 (매크로 감지 우회)**
- 아티스트 검색부터 결제까지 완전 자동화
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

### 방법 1: PyAutoGUI 전체 예매 자동화 (매크로 감지 우회) ⭐

브라우저 레벨에서 매크로 감지를 우회하기 위해 화면 좌표 기반으로 검색부터 결제까지 완전 자동화합니다.

#### 1단계: 좌표 설정
```bash
python coordinate_helper.py
```
- "새로운 좌표 설정" 선택
- 각 단계별로 마우스를 해당 위치로 이동하여 좌표 설정
- 좌표 저장 후 테스트 가능

#### 2단계: 전체 예매 자동화 실행
```bash
python main.py
# 선택: 5 (PyAutoGUI 전체 예매 자동화)
```

**자동화 과정:**
1. "PARK JIHOON" 검색
2. 첫 번째 상품 클릭
3. 예매 안내 팝업 확인
4. 날짜/회차 선택 (7월 12일 오후 7시)
5. STAGE 앞쪽 좌석 선택
6. 일반 1석 선택
7. 예매자 확인 사항 체크
8. 무통장입금 결제 진행

**⚠️ 주의사항:**
- 티켓링크 홈페이지에 이미 접속되어 있어야 함
- 로그인이 완료된 상태여야 함
- 긴급 정지: 마우스를 화면 모서리로 이동하면 프로그램 중단

### 방법 2: 기존 크롬 세션 활용 (권장)

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

### 방법 3: 자동 로그인

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

### 메인 프로그램 (main.py)
1. **로그인 테스트만** - 로그인 기능만 테스트
2. **전체 예매 테스트** - 로그인부터 예매까지 전체 과정 테스트
3. **직접 PAYCO 로그인 테스트** - PAYCO 로그인만 테스트
4. **기존 크롬 세션 활용 (권장)** - 이미 로그인된 크롬 창 활용
5. **PyAutoGUI 전체 예매 자동화** - 검색부터 결제까지 완전 자동화 ⭐

### PyAutoGUI 매크로 모드
- **좌표 보정만** - 마우스 좌표 설정
- **전체 예매 자동화 (PARK JIHOON)** - 검색부터 결제까지 완전 자동화

### 좌표 설정 헬퍼 (coordinate_helper.py)
- **새로운 좌표 설정** - 단계별 좌표 설정
- **저장된 좌표 로드** - 기존 좌표 불러오기
- **좌표 목록 표시** - 설정된 좌표 확인
- **좌표 테스트** - 마우스 이동으로 좌표 검증

## 🔍 문제 해결

### 매크로 감지 문제
- 티켓링크에서 "시스템에서 비정상적인 활동이 감지되었습니다" Alert 발생 시
- **PyAutoGUI 기반 매크로를 사용하세요** - 브라우저 레벨에서 감지되지 않습니다

### PAYCO 로그인 문제
- PAYCO는 불규칙적으로 생년월일 인증, 문자 인증 등을 요구합니다
- **기존 크롬 세션 활용 방법을 권장합니다**

### Chrome 연결 오류
- 크롬이 디버깅 모드로 실행되지 않은 경우 발생
- `start_chrome_debug.bat`을 실행하여 크롬을 재시작하세요

### Python 버전 문제
- Python 3.13에서는 `undetected_chromedriver` 호환성 문제가 있을 수 있습니다
- Python 3.12 이하 버전 사용을 권장합니다

### PyAutoGUI 좌표 문제
- 화면 해상도가 다르거나 브라우저 창 크기가 변경된 경우 좌표 재보정 필요
- `coordinate_helper.py`를 사용하여 좌표를 다시 설정하세요
- 좌표 테스트 기능으로 정확성 검증 가능

### 자동화 실패 문제
- 각 단계별로 실패 시 해당 좌표를 다시 설정하세요
- 브라우저 창 크기나 위치가 변경되지 않도록 주의하세요
- 네트워크 지연이나 페이지 로딩 시간을 고려하여 대기 시간 조정

## ⚠️ 주의사항

- 이 프로그램은 교육 목적으로 제작되었습니다
- 실제 사용 시에는 해당 웹사이트의 이용약관을 준수해주세요
- 과도한 요청으로 인한 서버 부하를 방지하기 위해 적절한 딜레이를 설정해주세요
- 매크로 감지 시스템이 있을 수 있으니 주의해서 사용하세요
- **PyAutoGUI 사용 시 긴급 정지: 마우스를 화면 모서리로 이동하면 프로그램이 중단됩니다**
- **전체 예매 자동화 사용 시 반드시 사전에 로그인을 완료해주세요**

## 📁 파일 구조

```
TicketLinkLauncher/
├── main.py                    # 메인 실행 파일
├── ticketlink_bot.py          # 티켓링크 봇 클래스 (Selenium 기반)
├── chrome_session_manager.py  # 크롬 세션 관리 모듈
├── ticketlink_pyautogui.py    # PyAutoGUI 기반 전체 예매 자동화 ⭐
├── coordinate_helper.py       # 좌표 설정 헬퍼
├── use_existing_chrome.py     # 기존 크롬 세션 활용 스크립트
├── start_chrome_debug.bat     # 크롬 디버깅 모드 시작 배치 파일
├── test_payco_login.py        # PAYCO 로그인 테스트
├── coordinates.json           # 저장된 좌표 (자동 생성)
├── requirements.txt           # 필요한 패키지 목록
├── .env                       # 환경 변수 (사용자가 생성)
├── env.example               # 환경 변수 예시
└── utils/
    ├── __init__.py
    └── logger.py             # 로깅 유틸리티
```

## 🛠️ 개발 환경

- Python 3.8+
- Chrome 브라우저
- Selenium WebDriver
- PyAutoGUI (화면 자동화)
- OpenCV (이미지 인식)
- undetected-chromedriver (선택사항)

## 📄 라이선스

MIT License

## 🤝 기여

버그 리포트나 기능 제안은 이슈를 통해 해주세요. 