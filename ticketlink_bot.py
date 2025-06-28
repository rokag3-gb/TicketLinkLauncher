#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TicketLink Bot - 티켓링크 웹사이트 자동화 클래스
"""

import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import setup_logger
import undetected_chromedriver as uc

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
        """웹드라이버 설정 - 매크로 감지 우회"""
        try:
            options = uc.ChromeOptions()
            # 헤드리스 모드 비활성화 (디버깅용)
            # chrome_options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # 매크로 감지 우회를 위한 설정
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0,
                "profile.managed_default_content_settings.images": 2
            })
            
            self.driver = uc.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 15)
            
            self.logger.info("웹드라이버 설정 완료 (undetected-chromedriver 사용)")
            
        except Exception as e:
            self.logger.error(f"웹드라이버 설정 실패: {e}")
            raise
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """랜덤 지연 시간"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def human_like_typing(self, element, text):
        """사람처럼 타이핑"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def human_like_click(self, element):
        """사람처럼 클릭"""
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.pause(random.uniform(0.1, 0.3))
        actions.click()
        actions.perform()
    
    def login(self):
        """로그인 수행"""
        try:
            self.logger.info("로그인 시도 중...")
            
            # 로그인 페이지로 이동
            login_url = f"{self.base_url}/user/login"
            self.driver.get(login_url)
            self.random_delay(2, 4)
            
            # 로그인 폼 요소 찾기
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "userId"))
            )
            password_field = self.driver.find_element(By.NAME, "userPw")
            
            # 사람처럼 로그인 정보 입력
            self.human_like_typing(username_field, self.username)
            self.random_delay(0.5, 1.5)
            self.human_like_typing(password_field, self.password)
            self.random_delay(1, 2)
            
            # 로그인 버튼 클릭
            login_button = self.driver.find_element(By.CLASS_NAME, "btn_login")
            self.human_like_click(login_button)
            
            # 로그인 성공 확인
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "user_info"))
            )
            
            self.logger.info("로그인 성공")
            
        except Exception as e:
            self.logger.error(f"로그인 실패: {e}")
            raise
    
    def go_to_product_page(self, product_url):
        """상품 페이지로 이동"""
        try:
            self.logger.info(f"상품 페이지로 이동: {product_url}")
            self.driver.get(product_url)
            self.random_delay(3, 5)
            
            # 페이지 로딩 대기
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "product_info"))
            )
            
            self.logger.info("상품 페이지 로딩 완료")
            
        except Exception as e:
            self.logger.error(f"상품 페이지 이동 실패: {e}")
            raise
    
    def select_date_and_time(self, target_date="8/15"):
        """날짜와 시간 선택"""
        try:
            self.logger.info(f"날짜 선택: {target_date}")
            
            # 날짜 선택 버튼 찾기
            date_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".date_btn, .calendar_date")
            
            target_found = False
            for button in date_buttons:
                if target_date in button.text or "8/15" in button.text:
                    self.human_like_click(button)
                    target_found = True
                    self.logger.info(f"날짜 선택 완료: {button.text}")
                    break
            
            if not target_found:
                self.logger.warning(f"대상 날짜 {target_date}를 찾을 수 없습니다. 첫 번째 가능한 날짜를 선택합니다.")
                if date_buttons:
                    self.human_like_click(date_buttons[0])
            
            self.random_delay(2, 4)
            
            # 시간 선택 (가장 빠른 시간)
            time_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".time_btn, .time_slot")
            if time_buttons:
                self.human_like_click(time_buttons[0])  # 첫 번째 시간 선택
                self.logger.info(f"시간 선택 완료: {time_buttons[0].text}")
            
            self.random_delay(2, 3)
            
        except Exception as e:
            self.logger.error(f"날짜/시간 선택 실패: {e}")
            raise
    
    def select_seats(self):
        """좌석 선택 - STAGE 제일 앞쪽"""
        try:
            self.logger.info("좌석 선택 시작")
            
            # 좌석 선택 버튼 클릭
            seat_select_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_seat_select, .seat_select_btn"))
            )
            self.human_like_click(seat_select_btn)
            
            self.random_delay(3, 5)
            
            # STAGE 좌석 찾기
            stage_seats = self.driver.find_elements(By.CSS_SELECTOR, ".seat.stage, .seat[data-area*='STAGE'], .seat[data-section*='STAGE']")
            
            if stage_seats:
                # STAGE 좌석 중 첫 번째(가장 앞쪽) 선택
                target_seat = stage_seats[0]
                self.human_like_click(target_seat)
                self.logger.info(f"STAGE 좌석 선택 완료: {target_seat.get_attribute('data-seat') or target_seat.text}")
            else:
                # STAGE 좌석을 찾을 수 없는 경우 일반 좌석 선택
                all_seats = self.driver.find_elements(By.CSS_SELECTOR, ".seat:not(.disabled):not(.sold)")
                if all_seats:
                    self.human_like_click(all_seats[0])
                    self.logger.info("일반 좌석 선택 완료")
            
            self.random_delay(2, 3)
            
            # 좌석 선택 완료 버튼
            confirm_btn = self.driver.find_element(By.CSS_SELECTOR, ".btn_confirm, .seat_confirm_btn")
            self.human_like_click(confirm_btn)
            
            self.logger.info("좌석 선택 완료")
            
        except Exception as e:
            self.logger.error(f"좌석 선택 실패: {e}")
            raise
    
    def proceed_to_payment(self):
        """결제 페이지로 진행"""
        try:
            self.logger.info("결제 페이지로 진행")
            
            # 예매 진행 버튼 클릭
            payment_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_payment, .btn_reserve, .btn_next"))
            )
            self.human_like_click(payment_btn)
            
            self.random_delay(3, 5)
            
            self.logger.info("결제 페이지 로딩 완료")
            
        except Exception as e:
            self.logger.error(f"결제 페이지 이동 실패: {e}")
            raise
    
    def select_payment_method(self):
        """결제 방법 선택 - PAYCO 간편결제 > 하나카드(6395)"""
        try:
            self.logger.info("결제 방법 선택")
            
            # PAYCO 간편결제 선택
            payco_option = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value*='PAYCO'], input[name*='payco'], .payco_option"))
            )
            self.human_like_click(payco_option)
            
            self.random_delay(1, 2)
            
            # 하나카드(6395) 선택
            card_options = self.driver.find_elements(By.CSS_SELECTOR, ".card_option, .card_select")
            for card in card_options:
                if "6395" in card.text or "하나카드" in card.text:
                    self.human_like_click(card)
                    self.logger.info("하나카드(6395) 선택 완료")
                    break
            
            self.random_delay(1, 2)
            
        except Exception as e:
            self.logger.error(f"결제 방법 선택 실패: {e}")
            raise
    
    def enter_payment_password(self, password="228080"):
        """결제 비밀번호 입력"""
        try:
            self.logger.info("결제 비밀번호 입력")
            
            # 비밀번호 입력 필드 찾기
            password_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password'], .password_input"))
            )
            
            self.human_like_typing(password_field, password)
            self.random_delay(1, 2)
            
            self.logger.info("결제 비밀번호 입력 완료")
            
        except Exception as e:
            self.logger.error(f"결제 비밀번호 입력 실패: {e}")
            raise
    
    def complete_payment(self):
        """결제 완료"""
        try:
            self.logger.info("결제 완료 버튼 클릭")
            
            # 결제 완료 버튼
            complete_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_pay, .btn_complete, .btn_final"))
            )
            self.human_like_click(complete_btn)
            
            self.random_delay(5, 8)
            
            self.logger.info("결제 완료 처리됨")
            
        except Exception as e:
            self.logger.error(f"결제 완료 실패: {e}")
            raise
    
    def run_test_booking(self, product_url):
        """테스트 예매 실행"""
        try:
            self.setup_driver()
            self.login()
            
            # 상품 페이지로 이동
            self.go_to_product_page(product_url)
            
            # 날짜/시간 선택
            self.select_date_and_time()
            
            # 좌석 선택
            self.select_seats()
            
            # 결제 페이지로 진행
            self.proceed_to_payment()
            
            # 결제 방법 선택
            self.select_payment_method()
            
            # 결제 비밀번호 입력
            self.enter_payment_password()
            
            # 결제 완료 (실제 결제는 하지 않고 확인만)
            self.logger.info("테스트 예매 과정 완료 - 실제 결제는 수행하지 않았습니다.")
            
            # 결과 확인을 위해 잠시 대기
            self.random_delay(10, 15)
            
        except Exception as e:
            self.logger.error(f"테스트 예매 중 오류 발생: {e}")
            raise
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("웹드라이버 종료")
    
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