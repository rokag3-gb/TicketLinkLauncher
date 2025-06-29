#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
티켓링크 PyAutoGUI 매크로 - 전체 예매 자동화
로그인된 상태에서 시작하여 검색부터 결제까지 완전 자동화
"""

import pyautogui
import time
import random
import os
from dotenv import load_dotenv
import cv2
import numpy as np
from PIL import Image

class TicketLinkPyAutoGUI:
    """PyAutoGUI를 사용한 티켓링크 전체 예매 자동화"""
    
    def __init__(self):
        """초기화"""
        # PyAutoGUI 설정
        pyautogui.FAILSAFE = True  # 마우스를 화면 모서리로 이동하면 중단
        pyautogui.PAUSE = 0.3  # 각 동작 사이 기본 대기 시간
        
        # 환경 변수 로드
        load_dotenv()
        
        # 화면 해상도 가져오기
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"🖥️ 화면 해상도: {self.screen_width}x{self.screen_height}")
        
        # 좌표 설정 (사용자가 조정해야 할 수 있음)
        self.coordinates = {
            # 검색 관련
            'search_box': (400, 100),  # 검색창 위치
            'search_button': (600, 100),  # 검색 버튼
            
            # 검색 결과 관련
            'first_product': (400, 300),  # 첫 번째 상품 클릭 위치
            
            # 예매 안내 팝업
            'popup_confirm': (500, 400),  # 팝업 확인 버튼
            
            # 날짜/회차 선택
            'date_time_select': (400, 350),  # 7월 12일 오후 7시 선택
            'booking_button': (500, 450),  # 예매하기 버튼
            
            # 좌석 선택
            'stage_front_seat': (400, 300),  # STAGE 앞쪽 좌석
            'next_step_seat': (600, 500),  # 다음단계 버튼 (좌석 선택 후)
            
            # 권종/할인/매수 선택
            'general_ticket': (400, 250),  # 일반 1석 선택
            'next_step_ticket': (600, 500),  # 다음단계 버튼 (권종 선택 후)
            
            # 예매자 확인 사항
            'all_checkboxes': (300, 200),  # 모든 체크박스
            'cancel_agreement': (300, 250),  # 취소기한및취소수수료동의
            'general_payment': (400, 300),  # 일반결제
            'payment_button': (500, 400),  # 결제하기 버튼
            
            # 결제 팝업
            'bank_transfer': (400, 200),  # 무통장입금
            'electronic_agreement': (300, 250),  # 전자금융거래 이용약관 동의
            'final_payment': (500, 350),  # 결제하기 버튼 (결제 팝업)
            'hana_bank': (400, 300),  # 하나은행
            'final_next': (500, 400),  # 다음 클릭 (최종)
        }
        
    def random_delay(self, min_seconds=0.5, max_seconds=2):
        """랜덤한 대기 시간"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def human_like_click(self, x, y, button='left'):
        """사람처럼 자연스러운 클릭"""
        # 랜덤한 오프셋 추가
        offset_x = random.randint(-3, 3)
        offset_y = random.randint(-3, 3)
        
        # 마우스 이동
        pyautogui.moveTo(x + offset_x, y + offset_y, duration=random.uniform(0.1, 0.2))
        self.random_delay(0.1, 0.2)
        
        # 클릭
        pyautogui.click(button=button)
        self.random_delay(0.3, 0.8)
        
    def human_like_typing(self, text, interval=0.05):
        """사람처럼 자연스러운 타이핑"""
        # 타이핑 전 짧은 대기
        self.random_delay(0.3, 0.6)
        
        # 기존 텍스트가 이미 선택되어 있을 수 있으므로 한 번 더 Ctrl+A
        pyautogui.hotkey('ctrl', 'a')
        self.random_delay(0.2, 0.4)
        
        # 텍스트 입력 (한 글자씩 자연스럽게)
        print(f"⌨️ 타이핑: {text}")
        for i, char in enumerate(text):
            pyautogui.typewrite(char)
            # 랜덤한 타이핑 속도 (사람처럼)
            time.sleep(random.uniform(0.05, 0.12))
            
            # 중간에 짧은 휴식 (자연스러움)
            if i > 0 and i % 3 == 0:
                time.sleep(random.uniform(0.1, 0.2))
        
        # 타이핑 완료 후 짧은 대기
        self.random_delay(0.5, 1.0)
        
    def search_for_artist(self, artist_name="PARK JIHOON"):
        """아티스트 검색"""
        try:
            print(f"🔍 '{artist_name}' 검색 중...")
            
            # 1. 검색창 클릭 (빈 곳 클릭)
            print("📍 검색창 클릭 중...")
            self.human_like_click(self.coordinates['search_box'][0], self.coordinates['search_box'][1])
            self.random_delay(1, 2)
            
            # 2. 기존 텍스트 삭제 (Ctrl+A)
            print("🗑️ 기존 텍스트 삭제 중...")
            pyautogui.hotkey('ctrl', 'a')
            self.random_delay(0.5, 1.0)
            
            # 3. 검색어 타이핑
            print(f"⌨️ '{artist_name}' 타이핑 중...")
            self.human_like_typing(artist_name)
            self.random_delay(1, 2)
            
            # 4. 검색 실행 (엔터키 또는 검색 아이콘 클릭)
            print("🔍 검색 실행 중...")
            
            # 먼저 엔터키 시도
            pyautogui.press('enter')
            self.random_delay(2, 3)
            
            # 엔터키가 작동하지 않을 경우 검색 아이콘 클릭
            print("🔍 검색 아이콘 클릭 시도...")
            self.human_like_click(self.coordinates['search_button'][0], self.coordinates['search_button'][1])
            self.random_delay(3, 5)
            
            # 5. 검색 결과 로딩 대기
            print("⏳ 검색 결과 로딩 대기 중...")
            self.random_delay(3, 5)
            
            print("✅ 검색 완료")
            return True
            
        except Exception as e:
            print(f"❌ 검색 실패: {e}")
            return False
            
    def click_first_product(self):
        """검색 결과 첫 번째 상품 클릭"""
        try:
            print("🎫 첫 번째 상품 클릭 중...")
            
            # 첫 번째 상품 클릭
            self.human_like_click(self.coordinates['first_product'][0], self.coordinates['first_product'][1])
            self.random_delay(2, 4)
            
            print("✅ 첫 번째 상품 클릭 완료")
            return True
            
        except Exception as e:
            print(f"❌ 첫 번째 상품 클릭 실패: {e}")
            return False
            
    def handle_booking_popup(self):
        """예매 안내 팝업 처리"""
        try:
            print("📋 예매 안내 팝업 처리 중...")
            
            # 팝업 확인 버튼 클릭
            self.human_like_click(self.coordinates['popup_confirm'][0], self.coordinates['popup_confirm'][1])
            self.random_delay(1, 2)
            
            print("✅ 팝업 처리 완료")
            return True
            
        except Exception as e:
            print(f"❌ 팝업 처리 실패: {e}")
            return False
            
    def select_date_and_time(self):
        """날짜와 회차 선택 (7월 12일 오후 7시)"""
        try:
            print("📅 날짜/회차 선택 중...")
            
            # 날짜/회차 선택 (7월 12일 오후 7시)
            self.human_like_click(self.coordinates['date_time_select'][0], self.coordinates['date_time_select'][1])
            self.random_delay(1, 2)
            
            # 예매하기 버튼 클릭
            self.human_like_click(self.coordinates['booking_button'][0], self.coordinates['booking_button'][1])
            self.random_delay(2, 4)
            
            print("✅ 날짜/회차 선택 완료")
            return True
            
        except Exception as e:
            print(f"❌ 날짜/회차 선택 실패: {e}")
            return False
            
    def select_seat(self):
        """좌석 선택 (STAGE 앞쪽)"""
        try:
            print("💺 좌석 선택 중...")
            
            # STAGE 앞쪽 좌석 클릭
            self.human_like_click(self.coordinates['stage_front_seat'][0], self.coordinates['stage_front_seat'][1])
            self.random_delay(1, 2)
            
            # 다음단계 버튼 클릭
            self.human_like_click(self.coordinates['next_step_seat'][0], self.coordinates['next_step_seat'][1])
            self.random_delay(2, 4)
            
            print("✅ 좌석 선택 완료")
            return True
            
        except Exception as e:
            print(f"❌ 좌석 선택 실패: {e}")
            return False
            
    def select_ticket_type(self):
        """권종/할인/매수 선택 (일반 1석)"""
        try:
            print("🎟️ 권종/할인/매수 선택 중...")
            
            # 일반 1석 선택
            self.human_like_click(self.coordinates['general_ticket'][0], self.coordinates['general_ticket'][1])
            self.random_delay(1, 2)
            
            # 다음단계 버튼 클릭
            self.human_like_click(self.coordinates['next_step_ticket'][0], self.coordinates['next_step_ticket'][1])
            self.random_delay(2, 4)
            
            print("✅ 권종/할인/매수 선택 완료")
            return True
            
        except Exception as e:
            print(f"❌ 권종/할인/매수 선택 실패: {e}")
            return False
            
    def fill_payment_info(self):
        """예매자 확인 사항 및 결제 정보 입력"""
        try:
            print("📝 예매자 확인 사항 및 결제 정보 입력 중...")
            
            # 모든 체크박스 클릭
            self.human_like_click(self.coordinates['all_checkboxes'][0], self.coordinates['all_checkboxes'][1])
            self.random_delay(0.5, 1.0)
            
            # 취소기한및취소수수료동의 체크
            self.human_like_click(self.coordinates['cancel_agreement'][0], self.coordinates['cancel_agreement'][1])
            self.random_delay(0.5, 1.0)
            
            # 일반결제 선택
            self.human_like_click(self.coordinates['general_payment'][0], self.coordinates['general_payment'][1])
            self.random_delay(0.5, 1.0)
            
            # 결제하기 버튼 클릭
            self.human_like_click(self.coordinates['payment_button'][0], self.coordinates['payment_button'][1])
            self.random_delay(2, 4)
            
            print("✅ 예매자 확인 사항 및 결제 정보 입력 완료")
            return True
            
        except Exception as e:
            print(f"❌ 예매자 확인 사항 및 결제 정보 입력 실패: {e}")
            return False
            
    def complete_payment(self):
        """결제 완료"""
        try:
            print("💳 결제 완료 중...")
            
            # 무통장입금 선택
            self.human_like_click(self.coordinates['bank_transfer'][0], self.coordinates['bank_transfer'][1])
            self.random_delay(1, 2)
            
            # 전자금융거래 이용약관 동의 체크
            self.human_like_click(self.coordinates['electronic_agreement'][0], self.coordinates['electronic_agreement'][1])
            self.random_delay(0.5, 1.0)
            
            # 결제하기 버튼 클릭 (결제 팝업)
            self.human_like_click(self.coordinates['final_payment'][0], self.coordinates['final_payment'][1])
            self.random_delay(2, 4)
            
            # 하나은행 선택
            self.human_like_click(self.coordinates['hana_bank'][0], self.coordinates['hana_bank'][1])
            self.random_delay(1, 2)
            
            # 다음 클릭 (최종)
            self.human_like_click(self.coordinates['final_next'][0], self.coordinates['final_next'][1])
            self.random_delay(2, 4)
            
            print("✅ 결제 완료!")
            return True
            
        except Exception as e:
            print(f"❌ 결제 완료 실패: {e}")
            return False
            
    def calibrate_coordinates(self):
        """좌표 보정 (사용자가 직접 설정)"""
        print("🎯 좌표 보정 모드")
        print("마우스를 해당 위치로 이동하고 Enter를 누르세요.")
        print("취소하려면 'q'를 누르세요.")
        
        coordinates_to_calibrate = [
            ('search_box', '검색창'),
            ('search_button', '검색 버튼'),
            ('first_product', '첫 번째 상품'),
            ('popup_confirm', '팝업 확인 버튼'),
            ('date_time_select', '날짜/회차 선택'),
            ('booking_button', '예매하기 버튼'),
            ('stage_front_seat', 'STAGE 앞쪽 좌석'),
            ('next_step_seat', '다음단계 버튼 (좌석)'),
            ('general_ticket', '일반 1석'),
            ('next_step_ticket', '다음단계 버튼 (권종)'),
            ('all_checkboxes', '모든 체크박스'),
            ('cancel_agreement', '취소기한및취소수수료동의'),
            ('general_payment', '일반결제'),
            ('payment_button', '결제하기 버튼'),
            ('bank_transfer', '무통장입금'),
            ('electronic_agreement', '전자금융거래 이용약관'),
            ('final_payment', '결제하기 버튼 (팝업)'),
            ('hana_bank', '하나은행'),
            ('final_next', '다음 클릭 (최종)')
        ]
        
        for coord_name, description in coordinates_to_calibrate:
            while True:
                user_input = input(f"{description} 위치로 마우스를 이동하고 Enter를 누르세요 (q로 취소): ")
                if user_input.lower() == 'q':
                    print("좌표 보정 취소됨")
                    return False
                elif user_input == '':
                    x, y = pyautogui.position()
                    self.coordinates[coord_name] = (x, y)
                    print(f"✅ {description} 좌표 설정: ({x}, {y})")
                    break
                    
        print("✅ 모든 좌표 보정 완료")
        return True
        
    def run_automation(self):
        """전체 예매 자동화 실행"""
        try:
            print("🚀 티켓링크 전체 예매 자동화 시작")
            print("=" * 60)
            print("⚠️ 주의사항:")
            print("1. 티켓링크 홈페이지에 이미 접속되어 있어야 합니다.")
            print("2. 로그인이 완료된 상태여야 합니다.")
            print("3. 긴급 정지: 마우스를 화면 모서리로 이동하세요.")
            print("=" * 60)
            
            # 사용자 확인
            confirm = input("위 조건을 모두 확인했습니다. 계속하시겠습니까? (y/n): ").strip().lower()
            if confirm != 'y':
                print("자동화가 취소되었습니다.")
                return False
                
            # 좌표 보정 여부 확인
            calibrate = input("좌표 보정을 하시겠습니까? (y/n): ").strip().lower()
            if calibrate == 'y':
                if not self.calibrate_coordinates():
                    return False
                    
            print("\n🎬 자동화 시작!")
            print("5초 후 시작됩니다...")
            time.sleep(5)
            
            # 1. 아티스트 검색
            if not self.search_for_artist("PARK JIHOON"):
                return False
                
            # 2. 첫 번째 상품 클릭
            if not self.click_first_product():
                return False
                
            # 3. 예매 안내 팝업 처리
            if not self.handle_booking_popup():
                return False
                
            # 4. 날짜/회차 선택
            if not self.select_date_and_time():
                return False
                
            # 5. 좌석 선택
            if not self.select_seat():
                return False
                
            # 6. 권종/할인/매수 선택
            if not self.select_ticket_type():
                return False
                
            # 7. 예매자 확인 사항 및 결제 정보 입력
            if not self.fill_payment_info():
                return False
                
            # 8. 결제 완료
            if not self.complete_payment():
                return False
                
            print("\n🎉 전체 예매 자동화 완료!")
            print("✅ PARK JIHOON 공연 예매가 성공적으로 완료되었습니다!")
            
            return True
            
        except Exception as e:
            print(f"❌ 자동화 실패: {e}")
            return False
            
    def emergency_stop(self):
        """긴급 정지"""
        print("🛑 긴급 정지!")
        pyautogui.FAILSAFE = True
        print("마우스를 화면 모서리로 이동하면 프로그램이 중단됩니다.")

def main():
    """메인 함수"""
    print("🎭 티켓링크 PyAutoGUI 전체 예매 자동화")
    print("=" * 60)
    
    # PyAutoGUI 매크로 인스턴스 생성
    macro = TicketLinkPyAutoGUI()
    
    try:
        # 긴급 정지 안내
        print("⚠️ 긴급 정지: 마우스를 화면 모서리로 이동하면 프로그램이 중단됩니다.")
        print("")
        
        # 실행 모드 선택
        print("실행 모드를 선택하세요:")
        print("1. 좌표 보정만")
        print("2. 전체 예매 자동화 (PARK JIHOON)")
        
        choice = input("선택 (1 또는 2): ").strip()
        
        if choice == "1":
            # 좌표 보정만
            macro.calibrate_coordinates()
            
        elif choice == "2":
            # 전체 예매 자동화
            macro.run_automation()
            
        else:
            print("❌ 잘못된 선택입니다.")
            
    except KeyboardInterrupt:
        print("\n⚠️ 프로그램이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        print("🔒 프로그램 종료")

if __name__ == "__main__":
    main() 