#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
로깅 설정 모듈
"""

import logging
import os
from datetime import datetime
from colorama import init, Fore, Style

# Colorama 초기화
init()

def setup_logger(name='ticketlink_bot', level=logging.INFO):
    """로거 설정"""
    
    # 로그 디렉토리 생성
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 로그 파일명 생성
    log_filename = f"{log_dir}/ticketlink_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 기존 핸들러 제거 (중복 방지)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 파일 핸들러 설정
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(level)
    
    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # 포맷터 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(ColoredFormatter())
    
    # 핸들러 추가
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

class ColoredFormatter(logging.Formatter):
    """컬러 출력을 위한 포맷터"""
    
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }
    
    def format(self, record):
        # 로그 레벨에 따른 색상 적용
        color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        
        return super().format(record) 