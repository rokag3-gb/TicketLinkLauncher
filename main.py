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
    print("Hello World!")
    print("티켓링크 매크로 프로그램을 시작합니다...")
    
    # 환경 변수 로드
    load_dotenv()
    
    # 로거 설정
    logger = setup_logger()
    logger.info("프로그램 시작")
    
    try:
        # 티켓링크 봇 인스턴스 생성
        bot = TicketLinkBot()
        
        # 봇 실행
        bot.run()
        
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