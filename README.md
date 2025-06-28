# TicketLink Launcher

티켓링크 웹사이트를 자동화하여 티켓 예매를 도와주는 Python 매크로 프로그램입니다.

## 기능

- 티켓링크 웹사이트 자동 접속
- 로그인 자동화
- 티켓 검색 및 예매 시도
- 예매 성공 시 알림 기능

## 설치 방법

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

## 사용 방법

1. `.env` 파일을 생성하고 필요한 설정을 입력합니다:
```
TICKETLINK_ID=your_id
TICKETLINK_PASSWORD=your_password
```

2. 프로그램을 실행합니다:
```bash
python main.py
```

## 주의사항

- 이 프로그램은 교육 목적으로 제작되었습니다.
- 실제 사용 시에는 해당 웹사이트의 이용약관을 준수해주세요.
- 과도한 요청으로 인한 서버 부하를 방지하기 위해 적절한 딜레이를 설정해주세요.

## 라이선스

MIT License

## 기여

버그 리포트나 기능 제안은 이슈를 통해 해주세요. 