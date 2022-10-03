# ---------------------------------------------------------------
import sys
import pyperclip
from pynput.keyboard import Key, Listener
import pyautogui
import win32con
import win32api
import time
from threading import Thread
from Point_Class import Point


# ---------------------------------------------------------------
class MyThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        # GuiAutomizer.name = name

        def on_press_esc(key):
            if key == Key.esc:
                print("------------------------- Завершение F -------------------------")
                # os._exit(0)
                sys.exit()

        # Collect events until released
        listener = Listener(on_press=on_press_esc)
        listener.start()

    def run(self):
        pass


# ---------------------------------------------------------------
class GuiAutomizer:
    @staticmethod
    def move(coords, delay=0.01):
        x = coords.x
        y = coords.y
        win32api.SetCursorPos((x, y))
        time.sleep(delay)

    @staticmethod
    def click(coords, delay=0.01):
        x = coords.x
        y = coords.y
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(delay)

    @staticmethod
    def click_right(coords, delay=0.01):
        x = coords.x
        y = coords.y
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
        time.sleep(delay)

    @staticmethod
    def dbl_click(coords, delay=0.01):
        x = coords.x
        y = coords.y
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(delay)

    @staticmethod
    def click_down(coords, delay=0.01):
        x = coords.x
        y = coords.y
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(delay)

    @staticmethod
    def click_up(coords, delay=0.01):
        x = coords.x
        y = coords.y
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(delay)

    # ---------------------------------------------------------------
    @staticmethod
    def hotkey(a, b):
        pyautogui.keyDown(a)
        time.sleep(0.1)
        pyautogui.keyDown(b)
        time.sleep(0.05)
        pyautogui.keyUp(b)
        time.sleep(0.02)
        pyautogui.keyUp(a)
        time.sleep(0.01)

    # ---------------------------------------------------------------
    @staticmethod
    def press_key(key, delay=0.01):
        pyautogui.press(key)
        if delay > 0:
            time.sleep(delay)

    # ---------------------------------------------------------------
    @staticmethod
    def press_keys(key1, key2, delay=0.01):
        GuiAutomizer.hotkey(key1, key2)
        if delay > 0:
            time.sleep(delay)

    # ---------------------------------------------------------------
    @staticmethod
    def pcad_reports():
        GuiAutomizer.press_keys('alt', 'tab', 0.8)
        GuiAutomizer.press_key('alt', 0.2)
        GuiAutomizer.press_key('right', 0.1)
        GuiAutomizer.press_key('enter', 0.1)
        for i in range(8):
            GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('enter')
        for i in range(3):
            GuiAutomizer.press_key('tab')
        GuiAutomizer.press_key('enter')
        for i in range(2):
            GuiAutomizer.press_keys('shift', 'tab')
        for i in range(7):
            GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('space')
        for i in range(8):
            GuiAutomizer.press_key('tab')
            if (i == 6) or (i == 5):
                GuiAutomizer.press_key('0')
        GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('up')
        GuiAutomizer.press_key('tab')
        GuiAutomizer.press_key('tab')
        GuiAutomizer.press_key('space', 1.5)
        GuiAutomizer.press_key('alt')
        GuiAutomizer.press_key('right')
        GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('up')
        GuiAutomizer.press_key('up')
        GuiAutomizer.press_key('enter')
        GuiAutomizer.press_key('alt')
        GuiAutomizer.press_key('right')
        GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('enter')
        GuiAutomizer.press_keys('alt', 'f4', 0.2)
        GuiAutomizer.press_key('tab')
        GuiAutomizer.press_key('enter')
        GuiAutomizer.press_key('alt')
        GuiAutomizer.press_keys('alt', 'tab')
        text = pyperclip.paste()
        return text

    # ---------------------------------------------------------------
    @staticmethod
    def pcad_correct_coords(arr_coords):
        # numberComp = int(input("Количество компонентов в PCAD файле: "))
        pyautogui.keyDown('alt')
        time.sleep(0.1)
        pyautogui.keyDown('tab')
        time.sleep(0.3)
        pyautogui.keyDown('tab')
        time.sleep(0.1)
        pyautogui.keyUp('alt')
        time.sleep(0.1)
        GuiAutomizer.press_key('alt')
        for i in range(2):
            GuiAutomizer.press_key('right')
        GuiAutomizer.press_key('enter')
        for i in range(4):
            GuiAutomizer.press_key('up')
        GuiAutomizer.press_key('enter', 0.2)
        exit_flag = False
        number = 0
        prev_ref = "NONE"
        while not exit_flag:
            # for i in range(7):
            GuiAutomizer.click(Point(x=839, y=366 - 40))  # scroll up
            GuiAutomizer.press_key('home', 0.1)
            time.sleep(0.1)
            GuiAutomizer.click(Point(x=882, y=366 - 40))  # select first ref
            time.sleep(0.1)
            pages = int(number / 15)  # 16 components in page
            for i in range(pages):
                GuiAutomizer.press_key('pagedown', 0.05)
            number_left = number - pages * 15
            for i in range(number_left):
                GuiAutomizer.press_key('down', 0)
            time.sleep(0.1)
            GuiAutomizer.click(Point(x=1025, y=370 - 40), 0.6)  # properties
            GuiAutomizer.click(Point(x=848, y=361 - 40), 0.1)  # ref
            GuiAutomizer.click(Point(x=848, y=361 - 40), 0.2)  # ref
            GuiAutomizer.press_keys('ctrl', 'c', 0.1)
            copied_ref = pyperclip.paste()
            print(number, copied_ref)
            if copied_ref == prev_ref:
                exit_flag = True
            else:
                prev_ref = copied_ref
                for coords in arr_coords:
                    # print(coords[2])
                    if copied_ref == coords[2]:
                        GuiAutomizer.click(Point(x=1059, y=538), 0.05)  # x
                        GuiAutomizer.click(Point(x=1059, y=538), 0.1)  # x
                        GuiAutomizer.press_keys('ctrl', 'x', 0.05)
                        copied_coord = pyperclip.paste()
                        x_new = round(float(copied_coord) + float(coords[0]), 3)
                        pyperclip.copy(str(x_new))
                        time.sleep(0.05)
                        GuiAutomizer.press_keys('ctrl', 'v', 0.2)
                        GuiAutomizer.press_key('tab')
                        GuiAutomizer.press_keys('ctrl', 'x', 0.05)
                        copied_coord = pyperclip.paste()
                        y_new = round(float(copied_coord) + float(coords[1]), 3)
                        pyperclip.copy(str(y_new))
                        time.sleep(0.05)
                        print("x: ", x_new, "y: ", y_new)
                        GuiAutomizer.press_keys('ctrl', 'v', 0.2)
                        GuiAutomizer.press_key('enter')
                        break
                else:
                    GuiAutomizer.press_key('enter')
                number += 1
        for i in range(6):
            GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('enter', 0.1)
        # Reports
        GuiAutomizer.press_key('alt', 0.2)
        GuiAutomizer.press_key('right', 0.1)
        GuiAutomizer.press_key('enter', 0.1)
        for i in range(8):
            GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('enter')
        for i in range(3):
            GuiAutomizer.press_key('tab')
        GuiAutomizer.press_key('enter')
        for i in range(2):
            GuiAutomizer.press_keys('shift', 'tab')
        for i in range(7):
            GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('space')
        for i in range(8):
            GuiAutomizer.press_key('tab')
            if (i == 6) or (i == 5):
                GuiAutomizer.press_key('0')
        GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('up')
        GuiAutomizer.press_key('tab')
        GuiAutomizer.press_key('tab')
        GuiAutomizer.press_key('space', 1.5)
        GuiAutomizer.press_key('alt')
        GuiAutomizer.press_key('right')
        GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('up')
        GuiAutomizer.press_key('up')
        GuiAutomizer.press_key('enter')
        GuiAutomizer.press_key('alt')
        GuiAutomizer.press_key('right')
        GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('down')
        GuiAutomizer.press_key('enter')
        GuiAutomizer.press_keys('alt', 'f4', 0.2)
        GuiAutomizer.press_key('tab')
        GuiAutomizer.press_key('enter')
        GuiAutomizer.press_key('alt')
        GuiAutomizer.press_keys('alt', 'tab')
        text = pyperclip.paste()
        return text

    # ---------------------------------------------------------------
