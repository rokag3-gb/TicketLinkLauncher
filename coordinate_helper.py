#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
좌표 설정 헬퍼 - 티켓링크 PyAutoGUI 매크로용
"""

import pyautogui
import time
import json
import os

class CoordinateHelper:
    """좌표 설정을 도와주는 클래스"""
    
    def __init__(self):
        """초기화"""
        self.coordinates = {}
        self.config_file = "coordinates.json"
        
    def get_mouse_position(self, description):
        """마우스 위치 가져오기"""
        print(f"\n📍 {description} 위치로 마우스를 이동하세요.")
        print("3초 후 현재 마우스 위치를 저장합니다...")
        
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
            
        x, y = pyautogui.position()
        print(f"✅ {description} 좌표 저장: ({x}, {y})")
        return x, y
        
    def setup_coordinates(self):
        """전체 좌표 설정"""
        print("🎯 티켓링크 PyAutoGUI 매크로 좌표 설정")
        print("=" * 50)
        print("각 단계별로 마우스를 해당 위치로 이동해주세요.")
        print("=" * 50)
        
        # 좌표 설정 목록
        coordinate_list = [
            ('search_box', '검색창'),
            ('search_button', '검색 버튼'),
            ('first_product', '첫 번째 상품'),
            ('popup_confirm', '팝업 확인 버튼'),
            ('date_time_select', '날짜/회차 선택 (7월 12일 오후 7시)'),
            ('booking_button', '예매하기 버튼'),
            ('stage_front_seat', 'STAGE 앞쪽 좌석'),
            ('next_step_seat', '다음단계 버튼 (좌석 선택 후)'),
            ('general_ticket', '일반 1석'),
            ('next_step_ticket', '다음단계 버튼 (권종 선택 후)'),
            ('all_checkboxes', '모든 체크박스'),
            ('cancel_agreement', '취소기한및취소수수료동의'),
            ('general_payment', '일반결제'),
            ('payment_button', '결제하기 버튼'),
            ('bank_transfer', '무통장입금'),
            ('electronic_agreement', '전자금융거래 이용약관'),
            ('final_payment', '결제하기 버튼 (결제 팝업)'),
            ('hana_bank', '하나은행'),
            ('final_next', '다음 클릭 (최종)')
        ]
        
        for coord_name, description in coordinate_list:
            print(f"\n{'-' * 30}")
            print(f"단계 {coordinate_list.index((coord_name, description)) + 1}/{len(coordinate_list)}")
            
            while True:
                user_input = input(f"{description} 위치로 마우스를 이동하고 Enter를 누르세요 (s로 건너뛰기, q로 취소): ").strip().lower()
                
                if user_input == 'q':
                    print("좌표 설정이 취소되었습니다.")
                    return False
                elif user_input == 's':
                    print(f"⏭️ {description} 건너뛰기")
                    break
                elif user_input == '':
                    x, y = self.get_mouse_position(description)
                    self.coordinates[coord_name] = (x, y)
                    break
                else:
                    print("❌ 잘못된 입력입니다. Enter, 's', 또는 'q'를 입력하세요.")
                    
        print("\n✅ 모든 좌표 설정 완료!")
        return True
        
    def save_coordinates(self):
        """좌표를 파일에 저장"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.coordinates, f, ensure_ascii=False, indent=2)
            print(f"💾 좌표가 {self.config_file}에 저장되었습니다.")
            return True
        except Exception as e:
            print(f"❌ 좌표 저장 실패: {e}")
            return False
            
    def load_coordinates(self):
        """파일에서 좌표 로드"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.coordinates = json.load(f)
                print(f"📂 좌표를 {self.config_file}에서 로드했습니다.")
                return True
            else:
                print(f"📂 {self.config_file} 파일이 없습니다.")
                return False
        except Exception as e:
            print(f"❌ 좌표 로드 실패: {e}")
            return False
            
    def display_coordinates(self):
        """저장된 좌표 표시"""
        if not self.coordinates:
            print("❌ 저장된 좌표가 없습니다.")
            return
            
        print("\n📋 저장된 좌표 목록:")
        print("=" * 40)
        for coord_name, (x, y) in self.coordinates.items():
            print(f"{coord_name}: ({x}, {y})")
            
    def test_coordinates(self):
        """좌표 테스트 (마우스 이동)"""
        if not self.coordinates:
            print("❌ 저장된 좌표가 없습니다.")
            return
            
        print("\n🧪 좌표 테스트 모드")
        print("각 좌표로 마우스가 이동합니다. 3초간 대기 후 다음으로 이동합니다.")
        
        for coord_name, (x, y) in self.coordinates.items():
            print(f"\n📍 {coord_name} 좌표로 이동: ({x}, {y})")
            pyautogui.moveTo(x, y, duration=1)
            time.sleep(3)
            
        print("\n✅ 좌표 테스트 완료!")

def main():
    """메인 함수"""
    print("🎯 티켓링크 PyAutoGUI 좌표 설정 헬퍼")
    print("=" * 50)
    
    helper = CoordinateHelper()
    
    try:
        while True:
            print("\n실행할 작업을 선택하세요:")
            print("1. 새로운 좌표 설정")
            print("2. 저장된 좌표 로드")
            print("3. 좌표 목록 표시")
            print("4. 좌표 테스트 (마우스 이동)")
            print("5. 종료")
            
            choice = input("선택 (1-5): ").strip()
            
            if choice == "1":
                # 새로운 좌표 설정
                if helper.setup_coordinates():
                    save = input("좌표를 저장하시겠습니까? (y/n): ").strip().lower()
                    if save == 'y':
                        helper.save_coordinates()
                        
            elif choice == "2":
                # 저장된 좌표 로드
                helper.load_coordinates()
                
            elif choice == "3":
                # 좌표 목록 표시
                helper.display_coordinates()
                
            elif choice == "4":
                # 좌표 테스트
                helper.test_coordinates()
                
            elif choice == "5":
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
        print("🔒 프로그램 종료")

if __name__ == "__main__":
    main() 