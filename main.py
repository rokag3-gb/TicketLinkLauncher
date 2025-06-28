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
    
    # 테스트할 상품 URL
    test_product_url = "https://www.ticketlink.co.kr/product/56274"
    
    try:
        # 티켓링크 봇 인스턴스 생성
        bot = TicketLinkBot()
        
        # 테스트 예매 실행
        print(f"테스트 예매를 시작합니다: {test_product_url}")
        logger.info(f"테스트 예매 시작: {test_product_url}")
        
        bot.run_test_booking(test_product_url)
        
        print("테스트 예매가 완료되었습니다.")
        logger.info("테스트 예매 완료")
        
    except KeyboardInterrupt:
        print("\n프로그램이 사용자에 의해 중단되었습니다.")
        logger.info("프로그램 중단됨")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        logger.error(f"프로그램 오류: {e}")
    finally:
        logger.info("프로그램 종료")

if __name__ == "__main__":
    main() 