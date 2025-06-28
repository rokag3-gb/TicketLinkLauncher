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
        """웹드라이버 설정 - undetected_chromedriver 사용으로 매크로 감지 우회"""
        try:
            # undetected_chromedriver 옵션 설정
            options = uc.ChromeOptions()
            
            # 헤드리스 모드 비활성화 (디버깅용)
            # options.add_argument("--headless")
            
            # 기본 설정
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            
            # User-Agent 설정 (더 일반적인 것으로 변경)
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
            
            # 창 크기 설정
            options.add_argument("--window-size=1366,768")
            
            # 매크로 감지 우회를 위한 핵심 설정
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            
            # 추가 우회 설정
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-features=TranslateUI")
            options.add_argument("--disable-ipc-flooding-protection")
            options.add_argument("--disable-hang-monitor")
            options.add_argument("--disable-prompt-on-repost")
            options.add_argument("--disable-domain-reliability")
            options.add_argument("--disable-component-extensions-with-background-pages")
            options.add_argument("--disable-default-apps")
            options.add_argument("--disable-sync")
            options.add_argument("--disable-translate")
            options.add_argument("--no-first-run")
            options.add_argument("--no-default-browser-check")
            options.add_argument("--disable-background-networking")
            options.add_argument("--disable-client-side-phishing-detection")
            options.add_argument("--disable-component-update")
            options.add_argument("--disable-sync-preferences")
            options.add_argument("--metrics-recording-only")
            options.add_argument("--no-report-upload")
            options.add_argument("--disable-logging")
            options.add_argument("--silent")
            options.add_argument("--log-level=3")
            
            # undetected_chromedriver로 드라이버 생성
            self.driver = uc.Chrome(options=options, version_main=None)
            self.wait = WebDriverWait(self.driver, 15)
            
            # 추가적인 매크로 감지 우회 스크립트
            stealth_js = """
            // 기본 webdriver 속성 제거
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // plugins 속성 설정
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // languages 속성 설정
            Object.defineProperty(navigator, 'languages', {
                get: () => ['ko-KR', 'ko', 'en-US', 'en'],
            });
            
            // permissions 속성 설정
            Object.defineProperty(navigator, 'permissions', {
                get: () => ({
                    query: () => Promise.resolve({state: 'granted'})
                }),
            });
            
            // chrome 속성 설정
            Object.defineProperty(window, 'chrome', {
                writable: true,
                enumerable: true,
                configurable: true,
                value: {
                    runtime: {},
                    loadTimes: function() {},
                    csi: function() {},
                    app: {}
                }
            });
            
            // 자동화 관련 속성 제거
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            
            // 추가 속성 설정
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 8,
            });
            
            Object.defineProperty(navigator, 'deviceMemory', {
                get: () => 8,
            });
            
            Object.defineProperty(navigator, 'platform', {
                get: () => 'Win32',
            });
            
            Object.defineProperty(navigator, 'productSub', {
                get: () => '20030107',
            });
            
            Object.defineProperty(navigator, 'vendor', {
                get: () => 'Google Inc.',
            });
            
            Object.defineProperty(navigator, 'maxTouchPoints', {
                get: () => 0,
            });
            """
            
            self.driver.execute_script(stealth_js)
            
            self.logger.info("웹드라이버 설정 완료 (undetected_chromedriver 사용)")
            
        except Exception as e:
            self.logger.error(f"웹드라이버 설정 실패: {e}")
            raise
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """랜덤 지연 시간"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def human_like_typing(self, element, text):
        """사람처럼 타이핑 - 더 자연스러운 속도와 패턴"""
        # 기존 텍스트 클리어
        element.clear()
        self.random_delay(0.2, 0.5)
        
        # 사람처럼 타이핑
        for i, char in enumerate(text):
            element.send_keys(char)
            # 타이핑 속도 변화 (시작은 느리고, 중간은 빠르고, 끝은 다시 느리게)
            if i < len(text) * 0.3:  # 처음 30%
                time.sleep(random.uniform(0.08, 0.15))
            elif i > len(text) * 0.7:  # 마지막 30%
                time.sleep(random.uniform(0.08, 0.15))
            else:  # 중간 40%
                time.sleep(random.uniform(0.03, 0.08))
            
            # 가끔 실수하고 백스페이스 (5% 확률)
            if random.random() < 0.05:
                element.send_keys(Keys.BACKSPACE)
                time.sleep(random.uniform(0.1, 0.2))
                element.send_keys(char)
                time.sleep(random.uniform(0.05, 0.1))
    
    def human_like_click(self, element):
        """사람처럼 클릭 - 마우스 움직임과 클릭 패턴"""
        actions = ActionChains(self.driver)
        
        # 현재 마우스 위치에서 요소로 자연스럽게 이동
        actions.move_to_element(element)
        actions.pause(random.uniform(0.2, 0.5))
        
        # 가끔 마우스를 약간 움직였다가 다시 클릭 (더 자연스럽게)
        if random.random() < 0.3:
            actions.move_by_offset(random.randint(-5, 5), random.randint(-5, 5))
            actions.pause(random.uniform(0.1, 0.3))
            actions.move_to_element(element)
            actions.pause(random.uniform(0.1, 0.2))
        
        # 클릭
        actions.click()
        actions.perform()
        
        # 클릭 후 잠시 대기
        self.random_delay(0.5, 1.5)
    
    def login_direct_payco(self):
        """직접 PAYCO 로그인 URL로 접근하는 방법"""
        try:
            self.logger.info("직접 PAYCO 로그인 시도...")
            
            # PAYCO 로그인 URL 직접 접근
            payco_login_url = "https://id.payco.com/oauth2.0/authorize?serviceProviderCode=TKLINK&scope=&response_type=code&state=1e6c8e08fcc74327bcb3d9a18375d736&client_id=Z9Ur2WLH9rB59Gy4_cJ3&redirect_uri=https://www.ticketlink.co.kr/auth/callback?selfRedirect=N&userLocale=ko_KR"
            
            self.logger.info(f"PAYCO 로그인 페이지로 직접 이동: {payco_login_url}")
            self.driver.get(payco_login_url)
            self.random_delay(3, 5)
            
            # PAYCO 로그인 페이지에서 로그인 처리
            self.handle_payco_login()
            
            # 로그인 후 리다이렉트 대기
            self.logger.info("로그인 후 리다이렉트 대기 중...")
            self.random_delay(5, 8)
            
            # 현재 URL 확인
            current_url = self.driver.current_url
            self.logger.info(f"로그인 후 현재 URL: {current_url}")
            
            # 티켓링크로 리다이렉트되었는지 확인
            if "ticketlink.co.kr" in current_url:
                self.logger.info("티켓링크로 성공적으로 리다이렉트됨")
                return True
            else:
                self.logger.warning("티켓링크로 리다이렉트되지 않음")
                return False
                
        except Exception as e:
            self.logger.error(f"직접 PAYCO 로그인 실패: {e}")
            raise
    
    def login(self):
        """PAYCO 로그인 수행"""
        try:
            self.logger.info("PAYCO 로그인 시도 중...")
            
            # 메인 페이지로 이동
            main_url = self.base_url
            self.logger.info(f"메인 페이지로 이동: {main_url}/home")
            self.driver.get(main_url)
            self.random_delay(3, 6)  # 더 긴 대기 시간
            
            # Alert 처리
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                self.logger.warning(f"Alert 감지: {alert_text}")
                alert.accept()
                self.random_delay(1, 2)
            except:
                pass  # Alert가 없으면 무시
            
            # 자연스러운 사이트 탐색 (매크로 감지 우회)
            self.logger.info("자연스러운 사이트 탐색 시작...")
            self.natural_browsing()
            
            # 현재 URL 확인
            current_url = self.driver.current_url
            self.logger.info(f"현재 페이지 URL: {current_url}")
            
            # 페이지가 완전히 로드될 때까지 대기
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            
            # 로그인 버튼 찾기 (여러 가능한 선택자 시도)
            login_selectors = [
                ".btn_login", 
                ".login_btn", 
                "a[href*='login']", 
                "button[onclick*='login']",
                ".user_login",
                "#loginBtn",
                ".header_login",
                ".gnb_login",
                "a[title*='로그인']",
                "button[title*='로그인']"
            ]
            
            login_button = None
            for selector in login_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        login_button = elements[0]
                        self.logger.info(f"로그인 버튼 찾음: {selector}")
                        break
                except:
                    continue
            
            if not login_button:
                # 로그인 링크 직접 클릭 시도 (텍스트 기반)
                try:
                    login_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '로그인')]")
                    for element in login_elements:
                        if element.is_displayed() and element.is_enabled():
                            login_button = element
                            self.logger.info("로그인 텍스트 요소 찾음")
                            break
                except:
                    pass
            
            if not login_button:
                # 더 넓은 범위로 검색
                try:
                    login_button = self.driver.find_element(By.XPATH, "//a[contains(@href, 'login') or contains(@onclick, 'login')]")
                    self.logger.info("로그인 링크 찾음")
                except:
                    self.logger.error("로그인 버튼을 찾을 수 없습니다.")
                    # 현재 페이지의 모든 링크 출력 (디버깅용)
                    try:
                        all_links = self.driver.find_elements(By.TAG_NAME, "a")
                        self.logger.info(f"페이지의 모든 링크 수: {len(all_links)}")
                        for i, link in enumerate(all_links[:10]):  # 처음 10개만
                            try:
                                self.logger.info(f"링크 {i+1}: {link.text} - {link.get_attribute('href')}")
                            except:
                                pass
                    except:
                        pass
                    raise Exception("로그인 버튼을 찾을 수 없습니다.")
            
            # 로그인 버튼이 화면에 보이도록 스크롤
            self.driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            self.random_delay(1, 2)
            
            # 로그인 버튼 클릭
            self.logger.info("로그인 버튼 클릭 중...")
            self.human_like_click(login_button)
            self.random_delay(4, 7)  # 더 긴 대기 시간
            
            # Alert 처리
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                self.logger.warning(f"로그인 버튼 클릭 후 Alert: {alert_text}")
                alert.accept()
                self.random_delay(1, 2)
            except:
                pass
            
            # 팝업 창 처리
            self.logger.info("팝업 창 확인 중...")
            main_window = self.driver.current_window_handle
            
            # 팝업 창이 열릴 때까지 대기
            self.random_delay(3, 6)
            
            # 모든 창 핸들 가져오기
            all_windows = self.driver.window_handles
            
            if len(all_windows) > 1:
                # 팝업 창으로 전환
                popup_window = None
                for window in all_windows:
                    if window != main_window:
                        popup_window = window
                        break
                
                if popup_window:
                    self.driver.switch_to.window(popup_window)
                    self.logger.info("팝업 창으로 전환됨")
                    
                    # PAYCO 로그인 페이지에서 로그인 정보 입력
                    self.handle_payco_login()
                    
                    # OAuth 콜백 처리 대기
                    self.logger.info("OAuth 콜백 처리 대기 중...")
                    self.random_delay(6, 10)
                    
                    # 팝업 창이 자동으로 닫혔는지 확인
                    current_windows = self.driver.window_handles
                    if popup_window in current_windows:
                        # 팝업 창이 아직 열려있으면 수동으로 닫기
                        self.driver.close()
                        self.driver.switch_to.window(main_window)
                        self.logger.info("팝업 창 수동 닫기 및 메인 창으로 복귀")
                    else:
                        # 팝업 창이 자동으로 닫힘
                        self.driver.switch_to.window(main_window)
                        self.logger.info("팝업 창 자동 닫힘, 메인 창으로 복귀")
                else:
                    self.logger.error("팝업 창을 찾을 수 없습니다.")
                    raise Exception("팝업 창을 찾을 수 없습니다.")
            else:
                # 팝업이 아닌 경우 현재 페이지에서 로그인 시도
                self.logger.info("팝업 창이 없음, 현재 페이지에서 로그인 시도")
                self.handle_payco_login()
            
            # 로그인 성공 확인 (여러 방법 시도)
            self.logger.info("로그인 성공 확인 중...")
            success_indicators = [
                (By.CLASS_NAME, "user_info"),
                (By.CLASS_NAME, "user_profile"),
                (By.CLASS_NAME, "logout"),
                (By.XPATH, "//a[contains(text(), '로그아웃')]"),
                (By.XPATH, "//span[contains(text(), '님')]"),
                (By.XPATH, "//a[contains(text(), '마이페이지')]"),
                (By.XPATH, "//a[contains(text(), '예매내역')]")
            ]
            
            login_success = False
            for indicator in success_indicators:
                try:
                    self.wait.until(EC.presence_of_element_located(indicator))
                    self.logger.info(f"로그인 성공 확인됨: {indicator[1]}")
                    login_success = True
                    break
                except:
                    continue
            
            if not login_success:
                # URL 기반 확인
                current_url = self.driver.current_url
                if "callback" in current_url or "auth" in current_url:
                    self.logger.info("OAuth 콜백 URL에서 로그인 성공 확인")
                    login_success = True
                
            if not login_success:
                raise Exception("로그인 성공을 확인할 수 없습니다.")
            
            self.logger.info("로그인 성공")
            
        except Exception as e:
            self.logger.error(f"로그인 실패: {e}")
            # 현재 페이지 정보 출력
            try:
                current_url = self.driver.current_url
                page_title = self.driver.title
                self.logger.error(f"현재 페이지 URL: {current_url}")
                self.logger.error(f"페이지 제목: {page_title}")
            except:
                pass
            raise
    
    def natural_browsing(self):
        """자연스러운 사이트 탐색 (매크로 감지 우회)"""
        try:
            self.logger.info("자연스러운 사이트 탐색 시작...")
            
            # 메인 페이지에서 잠시 머물기
            self.random_delay(2, 4)
            
            # 페이지 스크롤 (자연스럽게)
            self.logger.info("페이지 스크롤 중...")
            scroll_height = self.driver.execute_script("return document.body.scrollHeight")
            current_position = 0
            scroll_step = random.randint(200, 400)
            
            while current_position < scroll_height:
                current_position += scroll_step
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                self.random_delay(0.5, 1.5)
            
            # 다시 위로 스크롤
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.random_delay(1, 2)
            
            # 메뉴 링크들 클릭 (자연스럽게)
            try:
                menu_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/product'], a[href*='/category'], a[href*='/event']")
                if menu_links:
                    # 1-2개 링크만 클릭
                    for i in range(min(2, len(menu_links))):
                        link = menu_links[i]
                        if link.is_displayed() and link.is_enabled():
                            self.logger.info(f"메뉴 링크 클릭: {link.text}")
                            self.human_like_click(link)
                            self.random_delay(2, 4)
                            
                            # 뒤로 가기
                            self.driver.back()
                            self.random_delay(2, 3)
                            break
            except:
                pass
            
            # 검색창에 마우스 올리기 (클릭하지 않고)
            try:
                search_box = self.driver.find_element(By.CSS_SELECTOR, "input[type='search'], input[placeholder*='검색'], .search_input")
                if search_box.is_displayed():
                    actions = ActionChains(self.driver)
                    actions.move_to_element(search_box)
                    actions.pause(random.uniform(0.5, 1.0))
                    actions.perform()
                    self.logger.info("검색창에 마우스 올림")
            except:
                pass
            
            self.logger.info("자연스러운 사이트 탐색 완료")
            
        except Exception as e:
            self.logger.warning(f"자연스러운 탐색 중 오류: {e}")
            pass  # 오류가 있어도 계속 진행
    
    def handle_payco_login(self):
        """PAYCO 로그인 페이지에서 로그인 처리"""
        try:
            self.logger.info("PAYCO 로그인 페이지 처리 중...")
            
            # 현재 URL 확인
            current_url = self.driver.current_url
            self.logger.info(f"PAYCO 페이지 URL: {current_url}")
            
            # PAYCO 로그인 폼 요소 찾기 (여러 가능한 선택자)
            username_selectors = [
                "input[name='userId']",
                "input[name='id']", 
                "input[name='email']",
                "input[type='email']",
                "#userId",
                "#id",
                "#email"
            ]
            
            password_selectors = [
                "input[name='userPw']",
                "input[name='password']",
                "input[name='pw']",
                "input[type='password']",
                "#userPw",
                "#password",
                "#pw"
            ]
            
            # 사용자명 필드 찾기
            username_field = None
            for selector in username_selectors:
                try:
                    username_field = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    self.logger.info(f"사용자명 필드 찾음: {selector}")
                    break
                except:
                    continue
            
            if not username_field:
                self.logger.error("사용자명 입력 필드를 찾을 수 없습니다.")
                raise Exception("사용자명 입력 필드를 찾을 수 없습니다.")
            
            # 비밀번호 필드 찾기
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    self.logger.info(f"비밀번호 필드 찾음: {selector}")
                    break
                except:
                    continue
            
            if not password_field:
                self.logger.error("비밀번호 입력 필드를 찾을 수 없습니다.")
                raise Exception("비밀번호 입력 필드를 찾을 수 없습니다.")
            
            # 로그인 정보 입력
            self.logger.info("로그인 정보 입력 중...")
            self.human_like_typing(username_field, self.username)
            self.random_delay(0.5, 1.5)
            self.human_like_typing(password_field, self.password)
            self.random_delay(1, 2)
            
            # 로그인 버튼 찾기 및 클릭
            login_button_selectors = [
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
                    login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    self.logger.info(f"로그인 버튼 찾음: {selector}")
                    break
                except:
                    continue
            
            if not login_button:
                # 텍스트로 로그인 버튼 찾기
                try:
                    login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
                    self.logger.info("로그인 텍스트 버튼 찾음")
                except:
                    self.logger.error("로그인 버튼을 찾을 수 없습니다.")
                    raise Exception("로그인 버튼을 찾을 수 없습니다.")
            
            # 로그인 버튼 클릭
            self.logger.info("PAYCO 로그인 버튼 클릭 중...")
            self.human_like_click(login_button)
            
            # 로그인 완료 대기
            self.random_delay(3, 5)
            
            self.logger.info("PAYCO 로그인 처리 완료")
            
        except Exception as e:
            self.logger.error(f"PAYCO 로그인 처리 실패: {e}")
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
    
    def test_login_only(self):
        """로그인만 테스트"""
        try:
            self.setup_driver()
            self.login()
            
            # 로그인 성공 확인을 위해 잠시 대기
            self.random_delay(5, 10)
            
            self.logger.info("로그인 테스트 완료")
            
        except Exception as e:
            self.logger.error(f"로그인 테스트 중 오류 발생: {e}")
            raise
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("웹드라이버 종료")
    
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