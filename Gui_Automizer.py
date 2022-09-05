import pyperclip
from pynput.keyboard import Key, Listener
import pyautogui
import win32con
import win32api
import time
from threading import Thread
from Solder_Paste import qPoint
import os


class MyThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

        def on_press_esc(key):
            if key == Key.esc:
                print("------------------------- Завершение F -------------------------")
                os._exit(0)
                return False

        # Collect events until released
        listener = Listener(on_press=on_press_esc)
        listener.start()

    def run(self):
        pass


def move(coords, delay=0.01):
    x = coords.x
    y = coords.y
    win32api.SetCursorPos((x, y))
    time.sleep(delay)


def click(coords, delay=0.01):
    x = coords.x
    y = coords.y
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(delay)


def click_right(coords, delay=0.01):
    x = coords.x
    y = coords.y
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
    time.sleep(delay)


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


def click_down(coords, delay=0.01):
    x = coords.x
    y = coords.y
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(delay)


def click_up(coords, delay=0.01):
    x = coords.x
    y = coords.y
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(delay)


# ---------------------------------------------------------------
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
def press_key(key, delay=0.01):
    pyautogui.press(key)
    if delay > 0:
        time.sleep(delay)


# ---------------------------------------------------------------
def press_keys(key1, key2, delay=0.01):
    hotkey(key1, key2)
    if delay > 0:
        time.sleep(delay)


def pcad_reports():
    press_keys('alt', 'tab', 0.8)
    press_key('alt', 0.2)
    press_key('right', 0.1)
    press_key('enter', 0.1)
    for i in range(8):
        press_key('down')
    press_key('enter')
    for i in range(3):
        press_key('tab')
    press_key('enter')
    for i in range(2):
        press_keys('shift', 'tab')
    for i in range(7):
        press_key('down')
    press_key('space')
    for i in range(8):
        press_key('tab')
        if (i == 6) or (i == 5):
            press_key('0')
    press_key('down')
    press_key('up')
    press_key('tab')
    press_key('tab')
    press_key('space', 1.5)
    press_key('alt')
    press_key('right')
    press_key('down')
    press_key('up')
    press_key('up')
    press_key('enter')
    press_key('alt')
    press_key('right')
    press_key('down')
    press_key('down')
    press_key('down')
    press_key('enter')
    press_keys('alt', 'f4', 0.2)
    press_key('tab')
    press_key('enter')
    press_key('alt')
    press_keys('alt', 'tab')
    text = pyperclip.paste()
    return text


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
    press_key('alt')
    for i in range(2):
        press_key('right')
    press_key('enter')
    for i in range(4):
        press_key('up')
    press_key('enter', 0.2)
    exit_flag = False
    number = 0
    prev_ref = "NONE"
    while not exit_flag:
        # for i in range(7):
        click(qPoint(x=839, y=366 - 40))  # scroll up
        press_key('home', 0.1)
        time.sleep(0.1)
        click(qPoint(x=882, y=366 - 40))  # select first ref
        time.sleep(0.1)
        pages = int(number / 15)  # 16 components in page
        for i in range(pages):
            press_key('pagedown', 0.05)
        number_left = number - pages * 15
        for i in range(number_left):
            press_key('down', 0)
        time.sleep(0.1)
        click(qPoint(x=1025, y=370 - 40), 0.6)  # properties
        click(qPoint(x=848, y=361 - 40), 0.1)  # ref
        click(qPoint(x=848, y=361 - 40), 0.2)  # ref
        press_keys('ctrl', 'c', 0.1)
        copied_ref = pyperclip.paste()
        print(number, copied_ref)
        if copied_ref == prev_ref:
            exit_flag = True
        else:
            prev_ref = copied_ref
            for coords in arr_coords:
                # print(coords[2])
                if copied_ref == coords[2]:
                    click(qPoint(x=1059, y=538), 0.05)  # x
                    click(qPoint(x=1059, y=538), 0.1)  # x
                    press_keys('ctrl', 'x', 0.05)
                    copied_coord = pyperclip.paste()
                    x_new = round(float(copied_coord) + float(coords[0]), 3)
                    pyperclip.copy(str(x_new))
                    time.sleep(0.05)
                    press_keys('ctrl', 'v', 0.2)
                    press_key('tab')
                    press_keys('ctrl', 'x', 0.05)
                    copied_coord = pyperclip.paste()
                    y_new = round(float(copied_coord) + float(coords[1]), 3)
                    pyperclip.copy(str(y_new))
                    time.sleep(0.05)
                    print("x: ", x_new, "y: ", y_new)
                    press_keys('ctrl', 'v', 0.2)
                    press_key('enter')
                    break
            else:
                press_key('enter')
            number += 1
        # exit_flag = True#!1111111111111111111111111111111111111
    # press_key('esc')
    for i in range(6):
        press_key('down')
    press_key('enter', 0.1)
    # Reports
    press_key('alt', 0.2)
    press_key('right', 0.1)
    press_key('enter', 0.1)
    for i in range(8):
        press_key('down')
    press_key('enter')
    for i in range(3):
        press_key('tab')
    press_key('enter')
    for i in range(2):
        press_keys('shift', 'tab')
    for i in range(7):
        press_key('down')
    press_key('space')
    for i in range(8):
        press_key('tab')
        if (i == 6) or (i == 5):
            press_key('0')
    press_key('down')
    press_key('up')
    press_key('tab')
    press_key('tab')
    press_key('space', 1.5)
    press_key('alt')
    press_key('right')
    press_key('down')
    press_key('up')
    press_key('up')
    press_key('enter')
    press_key('alt')
    press_key('right')
    press_key('down')
    press_key('down')
    press_key('down')
    press_key('enter')
    press_keys('alt', 'f4', 0.2)
    press_key('tab')
    press_key('enter')
    press_key('alt')
    press_keys('alt', 'tab')
    text = pyperclip.paste()
    return text
