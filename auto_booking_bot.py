#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
티켓링크 자동 예매 봇 - PyAutoGUI 기반
좌표 설정, 색상 감지, 슬랙 알림 기능 포함
"""

import pyautogui
import time
import random
import json
import os
import cv2
import numpy as np
from PIL import Image, ImageGrab
import requests
from datetime import datetime
import threading
from dotenv import load_dotenv
import keyboard  # 전역 단축키 감지용

class AutoBookingBot:
    """티켓링크 자동 예매 봇"""
    
    def __init__(self):
        """초기화"""
        # PyAutoGUI 설정
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.2
        
        # 환경 변수 로드
        load_dotenv()
        
        # 화면 해상도
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"🖥️ 화면 해상도: {self.screen_width}x{self.screen_height}")
        
        # 좌표 설정 파일
        self.coordinates_file = "booking_coordinates.json"
        self.coordinates = self.load_coordinates()
        
        # 색상 설정 (예약 가능석 감지용)
        self.available_seat_color = (193, 144, 72)  # 예약 가능석 색상 (BGR) 하늘색
        #self.available_seat_color = (87, 98, 245)  # 예약 가능석 색상 (BGR) 주황색
        self.color_tolerance = 30  # 색상 허용 오차
        
        # 슬랙 설정
        self.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        self.slack_channel = os.getenv('SLACK_CHANNEL', '#ticket-booking')
        
        # 실행 상태
        self.is_running = False
        self.booking_success = False
        
        # 새로고침 간격 설정
        self.refresh_intervals = [0.6, 0.8, 0.9]  # 0.6초, 0.8초, 0.9초
        
    def load_coordinates(self):
        """좌표 파일 로드"""
        default_coordinates = {
            # 좌석 선택 페이지
            'refresh_button': (100, 100),  # 새로고침 버튼
            'seat_area': {  # 좌석 영역 (모니터링할 영역)
                'x1': 200, 'y1': 200,
                'x2': 800, 'y2': 600
            },
            'next_step_seat': (600, 500),  # 다음단계 버튼 (좌석 선택 후)
            
            # 권종/할인/매수 선택 페이지
            'general_0_combo': (400, 250),  # 일반 0 콤보박스
            'general_1_option': (400, 280),  # 일반 0 밑의 1 옵션
            'next_step_ticket': (600, 500),  # 다음단계 버튼 (권종 선택 후)
            
            # 배송선택/예매확인 페이지
            'buyer_checkbox1': (300, 200),  # 예매자확인 체크박스 1
            'buyer_checkbox2': (300, 220),  # 예매자확인 체크박스 2
            'cancel_agreement': (300, 250),  # 취소기한및취소수수료동의
            'general_payment': (400, 300),  # 일반결제
            'payment_button': (500, 400),  # 결제하기 버튼
            
            # PAYCO 결제팝업
            'bank_transfer': (400, 200),  # 무통장입금
            'electronic_agreement': (300, 250),  # 전자금융거래 이용약관 동의
            'payco_payment_button': (500, 350),  # 결제하기 버튼 (PAYCO)
            'hana_bank': (400, 300),  # 하나은행
            'final_next': (500, 400),  # 다음 버튼 (최종)
        }
        
        try:
            if os.path.exists(self.coordinates_file):
                with open(self.coordinates_file, 'r', encoding='utf-8') as f:
                    loaded_coords = json.load(f)
                    # 기본값과 병합
                    default_coordinates.update(loaded_coords)
                    print(f"✅ 좌표 파일 로드 완료: {self.coordinates_file}")
            else:
                print(f"📝 기본 좌표 사용 (파일 없음: {self.coordinates_file})")
        except Exception as e:
            print(f"⚠️ 좌표 파일 로드 실패, 기본값 사용: {e}")
            
        return default_coordinates
    
    def save_coordinates(self):
        """좌표를 파일에 저장"""
        try:
            with open(self.coordinates_file, 'w', encoding='utf-8') as f:
                json.dump(self.coordinates, f, ensure_ascii=False, indent=2)
            print(f"💾 좌표 저장 완료: {self.coordinates_file}")
            return True
        except Exception as e:
            print(f"❌ 좌표 저장 실패: {e}")
            return False
    
    def random_delay(self, min_seconds=0.5, max_seconds=2):
        """랜덤한 대기 시간"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def click_like_human(self, x, y, button='left'):
        """사람처럼 자연스러운 클릭"""
        # 랜덤한 오프셋 추가
        offset_x = random.randint(-3, 3)
        offset_y = random.randint(-3, 3)
        
        # 마우스 이동
        pyautogui.moveTo(x + offset_x, y + offset_y, duration=random.uniform(0.1, 0.3))
        self.random_delay(0.16, 0.19)
        
        # 클릭
        pyautogui.click(button=button)
        self.random_delay(0.18, 0.2)
    
    def send_slack_message(self, message, is_success=True):
        """슬랙으로 메시지 전송"""
        if not self.slack_webhook_url:
            print(f"⚠️ 슬랙 웹훅 URL이 설정되지 않음: {message}")
            return False
        
        try:
            # 이모지와 상태 추가
            status_emoji = "✅" if is_success else "❌"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            payload = {
                "channel": self.slack_channel,
                "text": f"{status_emoji} *티켓링크 자동 예매 봇* - {timestamp}\n{message}",
                "username": "티켓링크 봇",
                "icon_emoji": ":ticket:"
            }
            
            response = requests.post(self.slack_webhook_url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"📤 슬랙 메시지 전송 성공: {message}")
                return True
            else:
                print(f"❌ 슬랙 메시지 전송 실패: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 슬랙 메시지 전송 오류: {e}")
            return False
    
    def detect_available_seat(self, area=None):
        """예약 가능한 좌석 감지"""
        try:
            if area is None:
                area = self.coordinates['seat_area']
            
            # 스크린샷 캡처
            screenshot = ImageGrab.grab(bbox=(area['x1'], area['y1'], area['x2'], area['y2']))
            screenshot_np = np.array(screenshot)
            
            # BGR로 변환 (OpenCV 형식)
            screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            # 예약 가능석 범위 정의 (BGR)
            lower_available = np.array([
                max(0, self.available_seat_color[0] - self.color_tolerance),
                max(0, self.available_seat_color[1] - self.color_tolerance),
                max(0, self.available_seat_color[2] - self.color_tolerance)
            ])
            upper_available = np.array([
                min(255, self.available_seat_color[0] + self.color_tolerance),
                min(255, self.available_seat_color[1] + self.color_tolerance),
                min(255, self.available_seat_color[2] + self.color_tolerance)
            ])
            
            # 예약 가능석 마스크 생성
            available_mask = cv2.inRange(screenshot_bgr, lower_available, upper_available)
            
            # 예약 가능석 픽셀 찾기
            available_pixels = cv2.findNonZero(available_mask)
            
            if available_pixels is not None and len(available_pixels) > 10:  # 최소 10픽셀 이상
                # 첫 번째 예약 가능석 픽셀 위치 반환
                center = available_pixels[0][0]
                global_x = area['x1'] + center[0]
                global_y = area['y1'] + center[1]
                
                print(f"🟢 예약 가능한 좌석 감지: ({global_x}, {global_y})")
                return (global_x, global_y)
            else:
                print("⚫ 예약 가능한 좌석 없음")
                return None
                
        except Exception as e:
            print(f"❌ 색상 감지 오류: {e}")
            return None
    
    def refresh_page(self):
        """페이지 새로고침"""
        try:
            print("🔄 페이지 새로고침 중...")
            self.click_like_human(
                self.coordinates['refresh_button'][0],
                self.coordinates['refresh_button'][1]
            )
            self.random_delay(1, 1.3)
            return True
        except Exception as e:
            print(f"❌ 새로고침 실패: {e}")
            return False
    
    def get_pixel_color(self, x, y):
        img = ImageGrab.grab().convert('RGB')
        r, g, b = img.getpixel((x, y))
        return (r, g, b)

    def is_next_button_selected(self):
        x, y = self.coordinates['next_step_seat']
        color = self.get_pixel_color(x, y)
        # 글꼴색이 흰색(255,255,255)이면 좌석 선택됨
        return color == (255, 255, 255)
    
    def select_available_seat(self):
        """사용 가능한 좌석 선택"""
        try:
            print("🔍 사용 가능한 좌석 검색 중...")
            
            # 예약 가능한 좌석 감지
            seat_position = self.detect_available_seat()
            
            if seat_position:
                print(f"🎯 좌석 선택: {seat_position}")
                x0, y0 = seat_position
                selected = False
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        self.click_like_human(x0 + dx, y0 + dy)
                        self.random_delay(0.03, 0.06)
                        if self.is_next_button_selected():
                            selected = True
                            break
                    if selected:
                        break
                # 다음단계 버튼 클릭
                print("➡️ 다음단계 버튼 클릭")
                self.click_like_human(
                    self.coordinates['next_step_seat'][0],
                    self.coordinates['next_step_seat'][1]
                )
                self.random_delay(0.17, 0.2)

                self.send_slack_message("🚀 예약가능석 선택 후 다음단계 클릭까지 완료되었습니다.", True)
                #return True  # 좌석 선택 후 바로 함수 종료
            else:
                print("❌ 사용 가능한 좌석 없음")
                return False
        except Exception as e:
            print(f"❌ 좌석 선택 실패: {e}")
            return False
    
    def select_ticket_type(self):
        """권종/할인/매수 선택"""
        try:
            print("🎫 권종/할인/매수 선택 중...")
            
            # 일반 0 콤보박스 클릭
            print("📋 일반 0 콤보박스 클릭")
            self.click_like_human(
                self.coordinates['general_0_combo'][0],
                self.coordinates['general_0_combo'][1]
            )
            self.random_delay(0.02, 0.03)
            
            # 일반 0 밑의 1 옵션 클릭
            print("1️⃣ 일반 1 옵션 클릭")
            self.click_like_human(
                self.coordinates['general_1_option'][0],
                self.coordinates['general_1_option'][1]
            )
            self.random_delay(0.02, 0.03)
            
            # 다음단계 버튼 클릭
            print("➡️ 다음단계 버튼 클릭")
            self.click_like_human(
                self.coordinates['next_step_ticket'][0],
                self.coordinates['next_step_ticket'][1]
            )
            self.random_delay(0.04, 0.07)
            
            return True
            
        except Exception as e:
            print(f"❌ 권종 선택 실패: {e}")
            return False
    
    def fill_payment_info(self):
        """배송선택/예매확인 페이지 처리"""
        try:
            print("📝 예매확인 정보 입력 중...")
            
            # 예매자확인 체크박스들 체크
            print("✅ 예매자확인 체크박스 1 체크")
            self.click_like_human(
                self.coordinates['buyer_checkbox1'][0],
                self.coordinates['buyer_checkbox1'][1]
            )
            self.random_delay(0.01, 0.02)
            
            print("✅ 예매자확인 체크박스 2 체크")
            self.click_like_human(
                self.coordinates['buyer_checkbox2'][0],
                self.coordinates['buyer_checkbox2'][1]
            )
            self.random_delay(0.01, 0.02)
            
            # 취소기한및취소수수료동의 체크
            print("✅ 취소기한및취소수수료동의 체크")
            self.click_like_human(
                self.coordinates['cancel_agreement'][0],
                self.coordinates['cancel_agreement'][1]
            )
            self.random_delay(0.01, 0.02)
            
            # 일반결제 선택
            print("💳 일반결제 선택")
            self.click_like_human(
                self.coordinates['general_payment'][0],
                self.coordinates['general_payment'][1]
            )
            self.random_delay(0.01, 0.02)
            
            # 결제하기 버튼 클릭
            print("💳 결제하기 버튼 클릭")
            self.click_like_human(
                self.coordinates['payment_button'][0],
                self.coordinates['payment_button'][1]
            )
            self.random_delay(0.5, 0.7)
            
            return True
            
        except Exception as e:
            print(f"❌ 예매확인 정보 입력 실패: {e}")
            return False
    
    def complete_payco_payment(self):
        """PAYCO 결제 완료"""
        try:
            print("🏦 PAYCO 결제 진행 중...")
            
            # 무통장입금 선택
            print("🏦 무통장입금 선택")
            self.click_like_human(
                self.coordinates['bank_transfer'][0],
                self.coordinates['bank_transfer'][1]
            )
            self.random_delay(0.12, 0.19)
            
            # 전자금융거래 이용약관 동의
            print("✅ 전자금융거래 이용약관 동의")
            self.click_like_human(
                self.coordinates['electronic_agreement'][0],
                self.coordinates['electronic_agreement'][1]
            )
            self.random_delay(0.12, 0.19)
            
            # 결제하기 버튼 클릭
            print("💳 결제하기 버튼 클릭")
            self.click_like_human(
                self.coordinates['payco_payment_button'][0],
                self.coordinates['payco_payment_button'][1]
            )
            self.random_delay(0.12, 0.19)
            
            # 하나은행 선택
            print("🏦 하나은행 선택")
            self.click_like_human(
                self.coordinates['hana_bank'][0],
                self.coordinates['hana_bank'][1]
            )
            self.random_delay(0.12, 0.19)
            
            # 다음 버튼 클릭 (최종)
            print("➡️ 다음 버튼 클릭 (최종)")
            self.click_like_human(
                self.coordinates['final_next'][0],
                self.coordinates['final_next'][1]
            )
            self.random_delay(0.12, 0.19)
            
            return True
            
        except Exception as e:
            print(f"❌ PAYCO 결제 실패: {e}")
            self.send_slack_message("❌ PAYCO 결제 단계에서 실패했습니다.", False)
            return False
    
    def run_booking_loop(self):
        """메인 예매 루프"""
        print("🚀 자동 예매 시작!")
        self.send_slack_message("자동 예매 봇이 시작되었습니다.")
        
        refresh_count = 0
        
        while self.is_running and not self.booking_success:
            try:
                refresh_count += 1
                print(f"\n🔄 새로고침 #{refresh_count}")
                
                # 랜덤한 간격으로 새로고침
                refresh_interval = random.choice(self.refresh_intervals)
                print(f"⏱️ {refresh_interval}초 대기 후 새로고침...")
                time.sleep(refresh_interval)
                
                # 페이지 새로고침
                if not self.refresh_page():
                    continue
                
                # 사용 가능한 좌석 검색
                if self.select_available_seat():
                    print("🎯 좌석 선택 성공! 다음 단계로 진행...")
                    # 이후 단계 진입하지 않고 루프 종료
                    break
                else:
                    print("⏳ 사용 가능한 좌석이 없습니다. 계속 모니터링...")
                
            except KeyboardInterrupt:
                print("\n⚠️ 사용자에 의해 중단되었습니다.")
                self.send_slack_message("⚠️ 자동 예매가 사용자에 의해 중단되었습니다.", False)
                break
            except Exception as e:
                print(f"❌ 예매 루프 오류: {e}")
                self.send_slack_message(f"❌ 예매 루프에서 오류가 발생했습니다: {str(e)}", False)
                time.sleep(5)  # 오류 시 5초 대기
        
        if not self.booking_success and self.is_running:
            self.send_slack_message("⏰ 자동 예매가 종료되었습니다. (성공하지 못함)", False)
        
        print("🏁 자동 예매 종료")
        os._exit(0)
    
    def start_hotkey_listener(self):
        def on_hotkey():
            print("\n🛑 Ctrl+Shift+0 단축키 감지됨! 자동 예매를 종료합니다.")
            self.is_running = False
            self.send_slack_message("⚠️ 단축키(Ctrl+Shift+0)로 자동 예매가 강제 종료되었습니다.", False)
            # 강제 종료
            os._exit(0)
        keyboard.add_hotkey('ctrl+shift+0', on_hotkey)
    
    def start_booking(self):
        """예매 시작"""
        if self.is_running:
            print("⚠️ 이미 실행 중입니다.")
            return
        
        self.is_running = True
        self.booking_success = False
        
        # 전역 단축키 리스너 시작
        self.start_hotkey_listener()
        
        # 별도 스레드에서 실행
        booking_thread = threading.Thread(target=self.run_booking_loop)
        booking_thread.daemon = True
        booking_thread.start()
        
        print("✅ 자동 예매가 시작되었습니다. 중단하려면 Ctrl+Shift+0을 누르세요.")
    
    def stop_booking(self):
        """예매 중단"""
        self.is_running = False
        print("🛑 자동 예매 중단 요청됨")
    
    def calibrate_coordinates(self):
        """좌표 보정 도구"""
        print("🎯 좌표 보정 모드")
        print("각 요소의 위치로 마우스를 이동하고 Enter를 누르세요.")
        print("건너뛰려면 's', 취소하려면 'q'를 입력하세요.")
        
        coordinate_items = [
            ('refresh_button', '새로고침 버튼'),
            ('next_step_seat', '다음단계 버튼 (좌석 선택 후)'),
            ('general_0_combo', '일반 0 콤보박스'),
            ('general_1_option', '일반 0 밑의 1 옵션'),
            ('next_step_ticket', '다음단계 버튼 (권종 선택 후)'),
            ('buyer_checkbox1', '예매자확인 체크박스 1'),
            ('buyer_checkbox2', '예매자확인 체크박스 2'),
            ('cancel_agreement', '취소기한및취소수수료동의'),
            ('general_payment', '일반결제'),
            ('payment_button', '결제하기 버튼'),
            ('bank_transfer', '무통장입금'),
            ('electronic_agreement', '전자금융거래 이용약관 동의'),
            ('payco_payment_button', '결제하기 버튼 (PAYCO)'),
            ('hana_bank', '하나은행'),
            ('final_next', '다음 버튼 (최종)')
        ]
        
        for coord_name, description in coordinate_items:
            while True:
                user_input = input(f"\n{description} 위치로 마우스를 이동하고 Enter를 누르세요 (s/q): ").strip().lower()
                
                if user_input == 'q':
                    print("좌표 보정이 취소되었습니다.")
                    return False
                elif user_input == 's':
                    print(f"⏭️ {description} 건너뛰기")
                    break
                elif user_input == '':
                    x, y = pyautogui.position()
                    self.coordinates[coord_name] = (x, y)
                    print(f"✅ {description} 좌표 저장: ({x}, {y})")
                    break
                else:
                    print("❌ 잘못된 입력입니다. Enter, 's', 또는 'q'를 입력하세요.")
        
        # 좌석 영역 설정
        print("\n좌석 모니터링 영역을 설정합니다.")
        print("좌석이 표시되는 영역의 왼쪽 상단 모서리로 마우스를 이동하세요.")
        input("Enter를 누르면 좌표를 저장합니다...")
        x1, y1 = pyautogui.position()
        
        print("좌석이 표시되는 영역의 오른쪽 하단 모서리로 마우스를 이동하세요.")
        input("Enter를 누르면 좌표를 저장합니다...")
        x2, y2 = pyautogui.position()
        
        self.coordinates['seat_area'] = {
            'x1': min(x1, x2), 'y1': min(y1, y2),
            'x2': max(x1, x2), 'y2': max(y1, y2)
        }
        
        print(f"✅ 좌석 영역 설정: ({x1}, {y1}) ~ ({x2}, {y2})")
        
        # 좌표 저장
        if self.save_coordinates():
            print("✅ 모든 좌표가 저장되었습니다.")
            return True
        else:
            print("❌ 좌표 저장에 실패했습니다.")
            return False

def main():
    """메인 함수"""
    print("🎫 티켓링크 자동 예매 봇")
    print("=" * 50)
    
    bot = AutoBookingBot()
    
    try:
        while True:
            print("\n실행할 작업을 선택하세요:")
            print("1. 자동 예매 시작")
            print("2. 좌표 보정")
            print("3. 색상 감지 테스트")
            print("4. 종료")
            
            choice = input("선택 (1-4): ").strip()
            
            if choice == "1":
                # 자동 예매 시작
                print("\n⚠️ 주의사항:")
                print("- 티켓링크 좌석선택 페이지가 열려있어야 합니다.")
                print("- 좌표가 올바르게 설정되어 있어야 합니다.")
                print("- 중단하려면 Ctrl+Shift+0을 누르세요.")
                
                confirm = input("\n자동 예매를 시작하시겠습니까? (y/n): ").strip().lower()
                if confirm == 'y':
                    bot.start_booking()
                    
                    try:
                        while bot.is_running:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        bot.stop_booking()
                        print("\n🛑 자동 예매가 중단되었습니다.")
                        
            elif choice == "2":
                # 좌표 보정
                bot.calibrate_coordinates()
                
            elif choice == "3":
                # 색상 감지 테스트
                print("🔍 색상 감지 테스트")
                print("좌석 영역에서 예약 가능한 좌석을 감지합니다.")
                input("Enter를 누르면 테스트를 시작합니다...")
                
                seat_position = bot.detect_available_seat()
                if seat_position:
                    print(f"✅ 예약 가능한 좌석 감지: {seat_position}")
                else:
                    print("❌ 예약 가능한 좌석을 찾을 수 없습니다.")
                    
            elif choice == "4":
                # 종료
                print("👋 프로그램을 종료합니다.")
                break
                
            else:
                print("❌ 잘못된 선택입니다.")
                
    except KeyboardInterrupt:
        print("\n⚠️ 프로그램이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        if bot.is_running:
            bot.stop_booking()
        print("🔒 프로그램 종료")

if __name__ == "__main__":
    main() 