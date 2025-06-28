#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TicketLink Launcher - 티켓링크 매크로 프로그램
"""

import sys
import os
from dotenv import load_dotenv
from ticketlink_bot import TicketLinkBot
from utils.logger import setup_logger

def main():
    """메인 함수"""
    print("티켓링크 매크로 프로그램을 시작합니다...")
    
    # 환경 변수 로드
    load_dotenv()
    
    # 로거 설정
    logger = setup_logger()
    logger.info("프로그램 시작")
    
    # 환경 변수 검증
    username = os.getenv('TICKETLINK_ID')
    password = os.getenv('TICKETLINK_PASSWORD')
    
    if not username or not password or username == 'your_ticketlink_id':
        print("❌ 로그인 정보가 설정되지 않았습니다.")
        print("📝 .env 파일을 생성하고 다음 정보를 입력해주세요:")
        print("   TICKETLINK_ID=실제_아이디")
        print("   TICKETLINK_PASSWORD=실제_비밀번호")
        print("💡 env.example 파일을 참고하세요.")
        logger.error("로그인 정보 미설정")
        return
    
    # 실행 모드 선택
    #print("\n실행 모드를 선택하세요:")
    #print("1. 로그인 테스트만")
    #print("2. 전체 예매 테스트")
    #print("3. 직접 PAYCO 로그인 테스트")
    
    try:
        #choice = input("선택 (1, 2 또는 3): ").strip()
        choice = "3"
    except KeyboardInterrupt:
        print("\n⚠️ 프로그램이 중단되었습니다.")
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
            print("❌ 잘못된 선택입니다. 1, 2 또는 3을 입력해주세요.")
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