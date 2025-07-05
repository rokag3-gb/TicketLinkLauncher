import pyautogui
from PIL import ImageGrab
import time

print("좌석 위에 마우스를 올리고 3초 후 색상을 추출합니다...")
time.sleep(3)
x, y = pyautogui.position()
img = ImageGrab.grab().convert('RGB')
r, g, b = img.getpixel((x, y))
print(f"마우스 위치: ({x}, {y})")
print(f"RGB: ({r}, {g}, {b}) / BGR: ({b}, {g}, {r})") 