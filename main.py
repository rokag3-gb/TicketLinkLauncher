#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TicketLink Launcher - 티켓링크 매크로 프로그램
"""

import os
from dotenv import load_dotenv
from ticketlink_bot import TicketLinkBot
from chrome_session_manager import test_existing_session, navigate_to_product_page
from utils.logger import setup_logger

def main():
    """메인 함수"""
    print("티켓링크 매크로 프로그램을 시작합니다...")
    
    # 환경 변수 로드
    load_dotenv()
    
    # 로거 설정
    logger = setup_logger()
    logger.info("프로그램 시작")
    
    # 실행 모드 선택
    print("\n실행 모드를 선택하세요:")
    print("1. 로그인 테스트만")
    print("2. 전체 예매 테스트")
    print("3. 직접 PAYCO 로그인 테스트")
    print("4. 기존 크롬 세션 활용 (권장)")
    print("5. PyAutoGUI 매크로 실행")
    
    try:
        choice = input("선택 (1, 2, 3, 4 또는 5): ").strip()
    except KeyboardInterrupt:
        print("\n⚠️ 프로그램이 중단되었습니다.")
        return
    
    if choice == "4":
        # 기존 크롬 세션 활용
        print("🔗 기존 크롬 세션을 활용합니다...")
        logger.info("기존 크롬 세션 활용 시작")
        
        if test_existing_session():
            print("✅ 기존 세션 테스트 성공!")
            print("📝 이제 수동으로 예매를 진행하거나 추가 자동화를 구현할 수 있습니다.")
            
            # 상품 페이지로 이동 예시
            product_url = "https://www.ticketlink.co.kr/product/56274"
            if navigate_to_product_page(product_url):
                print("🎉 상품 페이지 접근 성공!")
                print("⏳ 10초 대기 중... (크롬 창은 유지됩니다)")
                import time
                time.sleep(10)
        else:
            print("❌ 기존 세션 테스트 실패")
            print("💡 크롬에서 티켓링크에 로그인한 후 다시 시도해주세요.")
        
        logger.info("기존 크롬 세션 활용 완료")
        return
        
    elif choice == "5":
        # PyAutoGUI 매크로 실행
        print("🖱️ PyAutoGUI 전체 예매 자동화를 실행합니다...")
        logger.info("PyAutoGUI 전체 예매 자동화 실행")
        
        try:
            from ticketlink_pyautogui import TicketLinkPyAutoGUI
            macro = TicketLinkPyAutoGUI()
            
            print("⚠️ 주의사항:")
            print("1. 티켓링크 홈페이지에 이미 접속되어 있어야 합니다.")
            print("2. 로그인이 완료된 상태여야 합니다.")
            print("3. 긴급 정지: 마우스를 화면 모서리로 이동하세요.")
            print("")
            
            confirm = input("위 조건을 모두 확인했습니다. 계속하시겠습니까? (y/n): ").strip().lower()
            if confirm == 'y':
                macro.run_automation()
            else:
                print("자동화가 취소되었습니다.")
                
        except ImportError:
            print("❌ PyAutoGUI 모듈을 찾을 수 없습니다.")
            print("💡 pip install pyautogui opencv-python pillow numpy를 실행해주세요.")
        except Exception as e:
            print(f"❌ PyAutoGUI 매크로 실행 실패: {e}")
        
        logger.info("PyAutoGUI 전체 예매 자동화 완료")
        return
    
    # 기존 로직 (1, 2, 3번 선택)
    # 환경 변수 검증
    username = os.getenv('TICKETLINK_ID')
    password = os.getenv('TICKETLINK_PASSWORD')
    birthday = os.getenv('TICKETLINK_BIRTHDAY', '19820124')
    
    if not username or not password or username == 'your_ticketlink_id':
        print("❌ 로그인 정보가 설정되지 않았습니다.")
        print("📝 .env 파일을 생성하고 다음 정보를 입력해주세요:")
        print("   TICKETLINK_ID=실제_아이디")
        print("   TICKETLINK_PASSWORD=실제_비밀번호")
        print("   TICKETLINK_BIRTHDAY=19820124")
        print("💡 env.example 파일을 참고하세요.")
        logger.error("로그인 정보 미설정")
        return
    
    try:
        # 티켓링크 봇 인스턴스 생성
        bot = TicketLinkBot()
        
        if choice == "1":
            # 로그인 테스트만
            print("🔐 로그인 테스트를 시작합니다...")
            logger.info("로그인 테스트 시작")
            bot.test_login_only()
            print("✅ 로그인 테스트가 완료되었습니다.")
            logger.info("로그인 테스트 완료")
            
        elif choice == "2":
            # 전체 예매 테스트
            test_product_url = "https://www.ticketlink.co.kr/product/56274"
            print(f"🎫 전체 예매 테스트를 시작합니다: {test_product_url}")
            logger.info(f"전체 예매 테스트 시작: {test_product_url}")
            bot.run_test_booking(test_product_url)
            print("✅ 전체 예매 테스트가 완료되었습니다.")
            logger.info("전체 예매 테스트 완료")
            
        elif choice == "3":
            # 직접 PAYCO 로그인 테스트
            print("🔐 직접 PAYCO 로그인 테스트를 시작합니다...")
            logger.info("직접 PAYCO 로그인 테스트 시작")
            bot.setup_driver()
            success = bot.login_direct_payco()
            if success:
                print("✅ 직접 PAYCO 로그인이 성공했습니다.")
                logger.info("직접 PAYCO 로그인 성공")
            else:
                print("❌ 직접 PAYCO 로그인이 실패했습니다.")
                logger.error("직접 PAYCO 로그인 실패")
            bot.driver.quit()
            
        else:
            print("❌ 잘못된 선택입니다. 1, 2, 3, 4 또는 5를 입력해주세요.")
            return
        
    except KeyboardInterrupt:
        print("\n⚠️ 프로그램이 사용자에 의해 중단되었습니다.")
        logger.info("프로그램 중단됨")
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")
        logger.error(f"프로그램 오류: {e}")
    finally:
        logger.info("프로그램 종료")

if __name__ == "__main__":
    main() 