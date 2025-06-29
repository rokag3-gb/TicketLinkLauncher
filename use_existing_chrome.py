#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
이미 로그인된 크롬 창을 활용하는 티켓링크 매크로
"""

import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv

def connect_to_existing_chrome():
    """이미 실행 중인 크롬에 연결"""
    print("🔗 이미 실행 중인 크롬에 연결 중...")
    
    # Chrome Remote Debugging 옵션 설정
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        # 이미 실행 중인 크롬에 연결
        driver = webdriver.Chrome(options=options)
        print("✅ 기존 크롬 창에 연결 성공!")
        return driver
    except Exception as e:
        print(f"❌ 기존 크롬 창 연결 실패: {e}")
        return None

def start_chrome_with_debugging():
    """디버깅 모드로 크롬 시작"""
    print("🚀 디버깅 모드로 크롬을 시작합니다...")
    print("📝 다음 명령어를 실행하세요:")
    print("")
    print("1. 기존 크롬 창을 모두 닫으세요")
    print("2. 명령 프롬프트에서 다음 명령어를 실행하세요:")
    print("")
    print("   chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\\temp\\chrome_debug")
    print("")
    print("3. 새로 열린 크롬 창에서 티켓링크에 로그인하세요")
    print("4. 로그인 완료 후 이 스크립트를 다시 실행하세요")
    print("")
    input("준비가 완료되면 Enter를 눌러주세요...")

def test_ticketlink_access(driver):
    """티켓링크 접근 테스트"""
    try:
        print("🌐 티켓링크 접근 테스트 중...")
        
        # 티켓링크 메인 페이지로 이동
        driver.get("https://www.ticketlink.co.kr")
        time.sleep(3)
        
        current_url = driver.current_url
        print(f"🔗 현재 URL: {current_url}")
        
        # 로그인 상태 확인
        try:
            # 로그인된 상태를 나타내는 요소들 찾기
            login_indicators = [
                "//a[contains(text(), '로그아웃')]",
                "//span[contains(text(), '님')]",
                "//a[contains(text(), '마이페이지')]",
                "//a[contains(text(), '예매내역')]"
            ]
            
            for indicator in login_indicators:
                try:
                    element = driver.find_element(By.XPATH, indicator)
                    print(f"✅ 로그인 상태 확인됨: {element.text}")
                    return True
                except:
                    continue
            
            print("❌ 로그인되지 않은 상태입니다.")
            return False
            
        except Exception as e:
            print(f"❌ 로그인 상태 확인 실패: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 티켓링크 접근 실패: {e}")
        return False

def go_to_product_page(driver, product_url):
    """상품 페이지로 이동"""
    try:
        print(f"🎫 상품 페이지로 이동: {product_url}")
        driver.get(product_url)
        time.sleep(3)
        
        # 페이지 로딩 확인
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        print("✅ 상품 페이지 로딩 완료")
        return True
        
    except Exception as e:
        print(f"❌ 상품 페이지 이동 실패: {e}")
        return False

def main():
    """메인 함수"""
    print("🎭 티켓링크 매크로 (기존 크롬 세션 활용)")
    print("=" * 50)
    
    # 환경 변수 로드
    load_dotenv()
    
    # 드라이버 연결 시도
    driver = connect_to_existing_chrome()
    
    if not driver:
        print("❌ 기존 크롬 창에 연결할 수 없습니다.")
        start_chrome_with_debugging()
        return
    
    try:
        # 티켓링크 접근 테스트
        if not test_ticketlink_access(driver):
            print("❌ 티켓링크에 로그인되지 않은 상태입니다.")
            print("💡 크롬 창에서 티켓링크에 로그인한 후 다시 실행해주세요.")
            return
        
        print("✅ 로그인 상태 확인 완료!")
        
        # 상품 페이지로 이동
        product_url = "https://www.ticketlink.co.kr/product/56274"
        if go_to_product_page(driver, product_url):
            print("🎉 상품 페이지 접근 성공!")
            print("📝 이제 수동으로 예매를 진행하거나 추가 자동화를 구현할 수 있습니다.")
        
        # 잠시 대기
        print("⏳ 10초 대기 중...")
        time.sleep(10)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        print("🔒 프로그램 종료 (크롬 창은 유지됩니다)")

if __name__ == "__main__":
    main() 