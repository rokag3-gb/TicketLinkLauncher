#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAYCO 로그인 테스트 스크립트
"""

import undetected_chromedriver as uc
import time
import random
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv

def test_payco_login():
    """PAYCO 로그인 테스트"""
    print("🔍 PAYCO 로그인 테스트 시작...")
    
    # 환경 변수 로드
    load_dotenv()
    username = os.getenv('TICKETLINK_ID')
    password = os.getenv('TICKETLINK_PASSWORD')
    birthday = os.getenv('TICKETLINK_BIRTHDAY', '19820124')  # 기본값 설정
    
    if not username or not password:
        print("❌ 로그인 정보가 설정되지 않았습니다.")
        return
    
    driver = None
    try:
        # undetected_chromedriver 설정
        options = uc.ChromeOptions()
        options.add_argument("--window-size=1366,768")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        
        # 드라이버 생성
        driver = uc.Chrome(options=options, version_main=None)
        wait = WebDriverWait(driver, 15)
        
        print("✅ 드라이버 생성 성공")
        
        # PAYCO 로그인 URL 직접 접근
        payco_login_url = "https://id.payco.com/oauth2.0/authorize?serviceProviderCode=TKLINK&scope=&response_type=code&state=1e6c8e08fcc74327bcb3d9a18375d736&client_id=Z9Ur2WLH9rB59Gy4_cJ3&redirect_uri=https://www.ticketlink.co.kr/auth/callback?selfRedirect=N&userLocale=ko_KR"
        
        print(f"🌐 PAYCO 로그인 페이지로 이동: {payco_login_url}")
        driver.get(payco_login_url)
        time.sleep(3)
        
        print(f"📄 현재 페이지 제목: {driver.title}")
        print(f"🔗 현재 URL: {driver.current_url}")
        
        # 로그인 폼 요소 찾기
        print("🔍 로그인 폼 요소 찾는 중...")
        
        # 사용자명 필드 찾기
        username_selectors = [
            "input[name='userId']",
            "input[name='id']", 
            "input[name='email']",
            "input[type='email']",
            "#userId",
            "#id",
            "#email"
        ]
        
        username_field = None
        for selector in username_selectors:
            try:
                username_field = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                print(f"✅ 사용자명 필드 찾음: {selector}")
                break
            except:
                continue
        
        if not username_field:
            print("❌ 사용자명 입력 필드를 찾을 수 없습니다.")
            return
        
        # 비밀번호 필드 찾기
        password_selectors = [
            "input[name='userPw']",
            "input[name='password']",
            "input[name='pw']",
            "input[type='password']",
            "#userPw",
            "#password",
            "#pw"
        ]
        
        password_field = None
        for selector in password_selectors:
            try:
                password_field = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"✅ 비밀번호 필드 찾음: {selector}")
                break
            except:
                continue
        
        if not password_field:
            print("❌ 비밀번호 입력 필드를 찾을 수 없습니다.")
            return
        
        # 로그인 정보 입력
        print("⌨️ 로그인 정보 입력 중...")
        
        # 사용자명 입력
        username_field.clear()
        time.sleep(0.5)
        for char in username:
            username_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.1))
        
        time.sleep(1)
        
        # 비밀번호 입력
        password_field.clear()
        time.sleep(0.5)
        for char in password:
            password_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.1))
        
        time.sleep(1)
        
        # 로그인 버튼 찾기
        print("🔍 로그인 버튼 찾는 중...")
        login_button_selectors = [
            "#loginButton",  # PAYCO 로그인 버튼
            ".btn_login",
            ".login_btn", 
            "button[type='submit']",
            "input[type='submit']",
            ".btn_submit",
            "#loginBtn"
        ]
        
        login_button = None
        for selector in login_button_selectors:
            try:
                login_button = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"✅ 로그인 버튼 찾음: {selector}")
                break
            except:
                continue
        
        if not login_button:
            # 텍스트로 로그인 버튼 찾기
            try:
                login_button = driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
                print("✅ 로그인 텍스트 버튼 찾음")
            except:
                print("❌ 로그인 버튼을 찾을 수 없습니다.")
                return
        
        # 로그인 버튼 클릭
        print("🖱️ 로그인 버튼 클릭 중...")
        actions = ActionChains(driver)
        actions.move_to_element(login_button)
        actions.pause(0.5)
        actions.click()
        actions.perform()
        
        # 로그인 완료 대기
        print("⏳ 로그인 완료 대기 중...")
        time.sleep(5)
        
        # 생년월일 인증 처리 (새로운 기기/브라우저 감지 시)
        current_url = driver.current_url
        print(f"🔗 로그인 후 현재 URL: {current_url}")
        
        if "deviceEnvironment" in current_url or "certification" in current_url:
            print("🔐 생년월일 인증 페이지 감지됨")
            
            try:
                # 생년월일 입력 필드 찾기
                birthday_field = wait.until(
                    EC.presence_of_element_located((By.ID, "birthday"))
                )
                print("✅ 생년월일 입력 필드 찾음")
                
                # 생년월일 입력
                print(f"📅 생년월일 입력 중: {birthday}")
                birthday_field.clear()
                time.sleep(0.5)
                for char in birthday:
                    birthday_field.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.1))
                
                time.sleep(1)
                
                # 확인 버튼 클릭
                confirm_button = driver.find_element(By.ID, "confirmBtn")
                print("✅ 확인 버튼 찾음")
                
                print("🖱️ 확인 버튼 클릭 중...")
                actions = ActionChains(driver)
                actions.move_to_element(confirm_button)
                actions.pause(0.5)
                actions.click()
                actions.perform()
                
                # 인증 완료 대기
                print("⏳ 생년월일 인증 완료 대기 중...")
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ 생년월일 인증 처리 중 오류: {e}")
        
        # 최종 결과 확인
        current_url = driver.current_url
        print(f"🔗 최종 현재 URL: {current_url}")
        
        if "ticketlink.co.kr" in current_url:
            print("✅ 티켓링크로 성공적으로 리다이렉트됨")
            print("🎉 PAYCO 로그인 성공!")
        else:
            print("❌ 티켓링크로 리다이렉트되지 않음")
            print("📄 현재 페이지 제목:", driver.title)
        
        # 10초 대기
        print("⏳ 10초 대기 중...")
        time.sleep(10)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        if driver:
            driver.quit()
            print("🔒 드라이버 종료")

if __name__ == "__main__":
    test_payco_login() 