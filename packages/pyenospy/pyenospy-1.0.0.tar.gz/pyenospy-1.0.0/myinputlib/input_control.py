import win32api
import win32con
import time
from typing import Tuple

class MyInput:
    def __init__(self):
        """Basit mouse ve klavye kontrolü için sınıf başlatıcı"""
        pass

    def mouse_pos(self) -> Tuple[int, int]:
        """Mevcut mouse pozisyonunu döndürür"""
        return win32api.GetCursorPos()

    def mouse_move(self, x: int, y: int):
        """Mouse'u belirtilen koordinatlara taşır"""
        win32api.SetCursorPos((x, y))

    def mouse_click(self, button: str = 'left'):
        """Mouse tıklaması yapar
        Args:
            button: 'left', 'right' veya 'middle'
        """
        if button == 'left':
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        elif button == 'right':
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        elif button == 'middle':
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)

    def mouse_double_click(self):
        """Sol tuş ile çift tıklama yapar"""
        self.mouse_click('left')
        time.sleep(0.1)
        self.mouse_click('left')

    def key_press(self, key: str):
        """Belirtilen tuşa basar
        Args:
            key: Basılacak tuş (örn: 'a', 'enter', 'shift')
        """
        win32api.keybd_event(ord(key.upper()), 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(ord(key.upper()), 0, win32con.KEYEVENTF_KEYUP, 0)

    def key_down(self, key: str):
        """Belirtilen tuşu basılı tutar"""
        win32api.keybd_event(ord(key.upper()), 0, 0, 0)

    def key_up(self, key: str):
        """Basılı tutulan tuşu bırakır"""
        win32api.keybd_event(ord(key.upper()), 0, win32con.KEYEVENTF_KEYUP, 0)

    def type_text(self, text: str, delay: float = 0.1):
        """Metin yazar
        Args:
            text: Yazılacak metin
            delay: Tuşlar arası bekleme süresi (saniye)
        """
        for char in text:
            self.key_press(char)
            time.sleep(delay)

    def wait(self, seconds: float):
        """Belirtilen süre kadar bekler
        Args:
            seconds: Beklenecek süre (saniye)
        """
        time.sleep(seconds) 