#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TicketLink Bot - 티켓링크 웹사이트 자동화 클래스
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import setup_logger

class TicketLinkBot:
    """티켓링크 웹사이트 자동화 봇"""
    
    def __init__(self):
        """초기화"""
        self.logger = setup_logger()
        self.driver = None
        self.wait = None
        self.base_url = "https://www.ticketlink.co.kr"
        
        # 환경 변수에서 로그인 정보 가져오기
        self.username = os.getenv('TICKETLINK_ID')
        self.password = os.getenv('TICKETLINK_PASSWORD')
        
        if not self.username or not self.password:
            self.logger.error("로그인 정보가 설정되지 않았습니다. .env 파일을 확인해주세요.")
            raise ValueError("로그인 정보가 필요합니다.")
    
    def setup_driver(self):
        """웹드라이버 설정"""
        try:
            chrome_options = Options()
            # 헤드리스 모드 비활성화 (디버깅용)
            # chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 웹드라이버 생성
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # 대기 객체 생성
            self.wait = WebDriverWait(self.driver, 10)
            
            self.logger.info("웹드라이버 설정 완료")
            
        except Exception as e:
            self.logger.error(f"웹드라이버 설정 실패: {e}")
            raise
    
    def login(self):
        """로그인 수행"""
        try:
            self.logger.info("로그인 시도 중...")
            
            # 로그인 페이지로 이동
            login_url = f"{self.base_url}/user/login"
            self.driver.get(login_url)
            
            # 로그인 폼 요소 찾기
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "userId"))
            )
            password_field = self.driver.find_element(By.NAME, "userPw")
            
            # 로그인 정보 입력
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            
            # 로그인 버튼 클릭
            login_button = self.driver.find_element(By.CLASS_NAME, "btn_login")
            login_button.click()
            
            # 로그인 성공 확인
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "user_info"))
            )
            
            self.logger.info("로그인 성공")
            
        except Exception as e:
            self.logger.error(f"로그인 실패: {e}")
            raise
    
    def search_ticket(self, keyword):
        """티켓 검색"""
        try:
            self.logger.info(f"티켓 검색: {keyword}")
            
            # 검색 페이지로 이동
            search_url = f"{self.base_url}/search?keyword={keyword}"
            self.driver.get(search_url)
            
            # 검색 결과 대기
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "search_result"))
            )
            
            self.logger.info("티켓 검색 완료")
            
        except Exception as e:
            self.logger.error(f"티켓 검색 실패: {e}")
            raise
    
    def run(self):
        """메인 실행 함수"""
        try:
            self.setup_driver()
            self.login()
            
            # 예시: 특정 공연 검색
            self.search_ticket("뮤지컬")
            
            # 잠시 대기
            time.sleep(5)
            
        except Exception as e:
            self.logger.error(f"실행 중 오류 발생: {e}")
            raise
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("웹드라이버 종료") 