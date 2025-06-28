#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
설정 관리 모듈
"""

import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class Config:
    """설정 클래스"""
    
    # 티켓링크 설정
    TICKETLINK_BASE_URL = "https://www.ticketlink.co.kr"
    TICKETLINK_ID = os.getenv('TICKETLINK_ID')
    TICKETLINK_PASSWORD = os.getenv('TICKETLINK_PASSWORD')
    
    # 웹드라이버 설정
    HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'False').lower() == 'true'
    DRIVER_TIMEOUT = int(os.getenv('DRIVER_TIMEOUT', '10'))
    
    # 검색 설정
    SEARCH_KEYWORDS = os.getenv('SEARCH_KEYWORDS', '뮤지컬,연극,콘서트').split(',')
    SEARCH_INTERVAL = int(os.getenv('SEARCH_INTERVAL', '30'))  # 초
    
    # 알림 설정
    ENABLE_NOTIFICATIONS = os.getenv('ENABLE_NOTIFICATIONS', 'True').lower() == 'true'
    
    # 로깅 설정
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DIR = os.getenv('LOG_DIR', 'logs')
    
    @classmethod
    def validate(cls):
        """설정 유효성 검사"""
        if not cls.TICKETLINK_ID or not cls.TICKETLINK_PASSWORD:
            raise ValueError("TICKETLINK_ID와 TICKETLINK_PASSWORD가 필요합니다.")
        
        return True 