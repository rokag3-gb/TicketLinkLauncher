#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
기본 기능 테스트
"""

import unittest
import os
import sys
from dotenv import load_dotenv

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import setup_logger
from config import Config

class TestBasicFunctionality(unittest.TestCase):
    """기본 기능 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        load_dotenv()
        self.logger = setup_logger('test', level='DEBUG')
    
    def test_logger_setup(self):
        """로거 설정 테스트"""
        logger = setup_logger('test_logger')
        self.assertIsNotNone(logger)
        logger.info("테스트 로그 메시지")
    
    def test_config_loading(self):
        """설정 로딩 테스트"""
        # 기본 설정값 확인
        self.assertEqual(Config.TICKETLINK_BASE_URL, "https://www.ticketlink.co.kr")
        self.assertEqual(Config.DRIVER_TIMEOUT, 10)
        self.assertFalse(Config.HEADLESS_MODE)
    
    def test_hello_world(self):
        """Hello World 출력 테스트"""
        from main import main
        # main 함수가 정의되어 있는지 확인
        self.assertTrue(callable(main))

if __name__ == '__main__':
    unittest.main() 