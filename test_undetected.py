#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
undetected_chromedriver 테스트 스크립트
"""

import undetected_chromedriver as uc
import time
import random

def test_undetected_driver():
    """undetected_chromedriver 테스트"""
    print("🔍 undetected_chromedriver 테스트 시작...")
    
    try:
        # 옵션 설정
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # undetected_chromedriver 생성
        driver = uc.Chrome(options=options, version_main=None)
        
        print("✅ 드라이버 생성 성공")
        
        # 티켓링크 메인 페이지 접속
        print("🌐 티켓링크 메인 페이지 접속 중...")
        driver.get("https://www.ticketlink.co.kr")
        
        # 페이지 로딩 대기
        time.sleep(3)
        
        print(f"📄 현재 페이지 제목: {driver.title}")
        print(f"🔗 현재 URL: {driver.current_url}")
        
        # webdriver 속성 확인
        webdriver_detected = driver.execute_script("return navigator.webdriver")
        print(f"🤖 webdriver 감지 여부: {webdriver_detected}")
        
        # 10초 대기
        print("⏳ 10초 대기 중...")
        time.sleep(10)
        
        print("✅ 테스트 완료")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            print("🔒 드라이버 종료")

if __name__ == "__main__":
    test_undetected_driver() 