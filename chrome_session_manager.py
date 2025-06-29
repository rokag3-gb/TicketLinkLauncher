#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chrome 세션 관리 모듈
기존 크롬 창에 연결하고 세션을 관리하는 기능
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def connect_to_existing_chrome():
    """이미 실행 중인 크롬에 연결"""
    print("🔗 이미 실행 중인 크롬에 연결 중...")
    
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=options)
        print("✅ 기존 크롬 창에 연결 성공!")
        return driver
    except Exception as e:
        print(f"❌ 기존 크롬 창 연결 실패: {e}")
        return None

def handle_alert(driver):
    """Alert 처리"""
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"⚠️ Alert 감지: {alert_text}")
        
        # 매크로 감지 Alert인지 확인
        if "비정상적인 활동" in alert_text or "ErrorCode:200" in alert_text:
            print("🚨 매크로 감지 Alert 발견! 처리 중...")
            alert.accept()
            print("✅ Alert 처리 완료")
            return True
        else:
            # 일반 Alert 처리
            alert.accept()
            print("✅ 일반 Alert 처리 완료")
            return True
    except:
        # Alert가 없으면 False 반환
        return False

def natural_browsing(driver):
    """자연스러운 사이트 탐색 (매크로 감지 우회)"""
    try:
        print("🔄 자연스러운 사이트 탐색 시작...")
        
        # 랜덤한 대기 시간
        time.sleep(random.uniform(2, 4))
        
        # 마우스 움직임 시뮬레이션
        actions = ActionChains(driver)
        
        # 랜덤한 위치로 마우스 이동
        for _ in range(3):
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            actions.move_by_offset(x, y)
            actions.pause(random.uniform(0.5, 1.5))
        
        actions.perform()
        
        # 스크롤 시뮬레이션
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(random.uniform(1, 2))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1, 2))
        
        print("✅ 자연스러운 사이트 탐색 완료")
        
    except Exception as e:
        print(f"⚠️ 자연스러운 탐색 중 오류: {e}")

def test_existing_session():
    """기존 세션 테스트"""
    driver = connect_to_existing_chrome()
    if not driver:
        print("❌ 기존 크롬 창에 연결할 수 없습니다.")
        print("💡 start_chrome_debug.bat을 실행하여 크롬을 디버깅 모드로 시작하세요.")
        return False
    
    try:
        print("🌐 티켓링크 접근 테스트 중...")
        
        # 자연스러운 접근을 위해 랜덤 대기
        time.sleep(random.uniform(1, 3))
        
        driver.get("https://www.ticketlink.co.kr")
        time.sleep(5)  # 더 긴 대기 시간
        
        # Alert 처리
        if handle_alert(driver):
            print("🔄 Alert 처리 후 페이지 재로딩...")
            time.sleep(2)
            driver.refresh()
            time.sleep(3)
        
        # 자연스러운 사이트 탐색
        natural_browsing(driver)
        
        current_url = driver.current_url
        print(f"🔗 현재 URL: {current_url}")
        
        # 페이지 제목 확인
        try:
            title = driver.title
            print(f"🎫 페이지 제목: {title}")
        except:
            print("❌ 페이지 제목을 가져올 수 없습니다.")
        
        # 더 정확한 로그인 상태 확인
        print("🔍 로그인 상태 확인 중...")
        
        # 1. 로그아웃 링크 확인 (가장 확실한 지표)
        try:
            logout_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '로그아웃')]")
            if logout_elements:
                for element in logout_elements:
                    if element.is_displayed():
                        print(f"✅ 로그인 상태 확인됨: {element.text}")
                        return True
        except:
            pass
        
        # 2. 사용자 관련 텍스트 확인
        try:
            user_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '님')]")
            if user_elements:
                for element in user_elements:
                    if element.is_displayed():
                        print(f"✅ 로그인 상태 확인됨: {element.text}")
                        return True
        except:
            pass
        
        # 3. 마이페이지, 예매내역 등 사용자 전용 링크 확인
        user_links = ['마이페이지', '예매내역', '회원정보', '주문내역']
        for link_text in user_links:
            try:
                elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{link_text}')]")
                if elements:
                    for element in elements:
                        if element.is_displayed():
                            print(f"✅ 로그인 상태 확인됨: {element.text}")
                            return True
            except:
                continue
        
        # 4. 로그인 링크 확인 (로그인되지 않은 상태의 지표)
        try:
            login_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '로그인')]")
            if login_elements:
                for element in login_elements:
                    if element.is_displayed() and '로그아웃' not in element.text:
                        print("❌ 로그인되지 않은 상태입니다. (로그인 링크 발견)")
                        return False
        except:
            pass
        
        # 5. 페이지 소스에서 로그인 관련 키워드 검색
        try:
            page_source = driver.page_source.lower()
            if '로그아웃' in page_source or '님' in page_source or '마이페이지' in page_source:
                print("✅ 로그인 상태 확인됨 (페이지 소스에서 키워드 발견)")
                return True
            elif '로그인' in page_source and '로그아웃' not in page_source:
                print("❌ 로그인되지 않은 상태입니다. (페이지 소스에서 로그인 키워드만 발견)")
                return False
        except:
            pass
        
        # 6. 모든 링크 확인 (디버깅용)
        print("🔍 모든 링크 확인 중...")
        try:
            links = driver.find_elements(By.TAG_NAME, "a")
            print(f"📎 총 링크 개수: {len(links)}")
            
            login_related_links = []
            for link in links[:20]:  # 처음 20개만 확인
                try:
                    text = link.text.strip()
                    href = link.get_attribute("href")
                    if text and any(keyword in text.lower() for keyword in ['로그인', '로그아웃', '마이페이지', '회원가입', '예매내역']):
                        login_related_links.append({
                            'text': text,
                            'href': href
                        })
                except:
                    continue
            
            print(f"🔗 로그인 관련 링크: {len(login_related_links)}개")
            for link in login_related_links:
                print(f"   - {link['text']}: {link['href']}")
                
        except Exception as e:
            print(f"❌ 링크 확인 실패: {e}")
        
        print("❌ 로그인되지 않은 상태입니다.")
        return False
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        # Alert가 발생했을 가능성이 있으므로 다시 시도
        try:
            if handle_alert(driver):
                print("🔄 Alert 처리 후 재시도...")
                time.sleep(2)
                return test_existing_session()  # 재귀 호출로 재시도
        except:
            pass
        return False

def navigate_to_product_page(product_url):
    """상품 페이지로 이동"""
    try:
        driver = connect_to_existing_chrome()
        if not driver:
            return False
            
        print(f"🎫 상품 페이지로 이동: {product_url}")
        driver.get(product_url)
        time.sleep(3)
        
        print("✅ 상품 페이지 로딩 완료")
        return True
        
    except Exception as e:
        print(f"❌ 상품 페이지 이동 실패: {e}")
        return False 