# ==================================================================
import shutil
import math
import matplotlib.pyplot as plt
import random
import os
import win32con
import win32api
import win32file
from tkinter import *
import ctypes
import tkinter as tk
from tkinter import filedialog
import pyautogui
import time
from threading import Thread
import pyperclip
from pynput.keyboard import Key, Listener
# ==================================================================
# Import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
# ==============================================================================
correctX = 0
correctY = 0


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
        timer_exit = 0
        time.sleep(0.1)
        # print("ok")
        if timer_exit > 100:
            print("---------------- Аварийное завершение -------------------")
            os._exit(0)


# ***********************************************************************
class qPoint():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return qPoint(self.x + other.x, self.y + other.y)


# ---------------------------------------------------------------


def move(coords, delay=0.01):
    x = coords.x
    y = coords.y
    win32api.SetCursorPos((x, y))
    time.sleep(delay)


def click(coords, delay=0.01):
    x = coords.x + correctX
    y = coords.y + correctY
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


def press_keys(key1, key2, delay=0.01):
    hotkey(key1, key2)
    if delay > 0:
        time.sleep(delay)


# ***********************************************************************
threadExit = MyThread("exit")
threadExit.start()
# ***********************************************************************
ignoreRotation = False
useOnlyOneHead = False
# ***********************************************************************
NUMBER_NAME = "1"
NUMBER_RAZMER_X = "2"
NUMBER_RAZMER_Y = "3"
NUMBER_KOLVO_X = "4"
NUMBER_KOLVO_Y = "5"
NUMBER_SHOW_PLOT = "6"
NUMBER_SD_CHMT = "7"
NUMBER_SD_dispenser = "8"
NUMBER_SPLIT_SIZE = "9"
# LM358D - SO8 pic12f675
# 0.1 - 0.47
file_sd = "E:/"
allowConvert = 0
ignoreCoeff = 0
stackError = 0
coordCoef = 0.801
xCoef = 1.0
yCoef = 1.0
size_type_small = True
chmtXCoef = 1.0
chmtYCoef = 1.0
PI = 3.14159265
DOT_SMALL = 1
DOT_MEDIUM = 2
DOT_BIG = 3
LINE_START = 8
LINE_END = 9
# ***********************************************************************
DRIVE_REMOVABLE = 2
# ***********************************************************************

# ***********************************************************************
device_name = "test"
size_x = 1
size_y = 1
devices_number_x = 1
devices_number_y = 1
split_size_type = False
showPlot = False
copyToSdChmt = False
copyToSddispenser = False
KOLVO_KATUSHEK = 32
KOLVO_LOTKOV = 3
coils = [" "] * KOLVO_KATUSHEK
pathToFolder = os.path.abspath(__file__)
pathToFolderOutput = pathToFolder
FIRST_STRING = b'%,\xd4\xad\xb5\xe3\xc6\xab\xd2\xc6,X,Y,'
SECOND_STRING = b'%,\xc1\xcf\xd5\xbb\xc6\xab\xd2\xc6,\xc1\xcf\xd5\xbb\xba\xc5,X,Y,\xbd\xf8\xb8\xf8\xc1\xbf,' \
                b'\xd7\xa2\xca\xcd '
THIRD_STRING = b'%,\xc6\xb4\xb0\xe51,X,Y,'
FOURTH_STRING = b'%,\xcc\xf9\xcd\xb7\xba\xc5,\xc1\xcf\xd5\xbb\xba\xc5,X,Y,\xbd\xc7\xb6\xc8,\xb8\xdf\xb6\xc8,' \
                b'\xcc\xf8\xb9\xfd,\xcb\xd9\xb6\xc8,\xcb\xb5\xc3\xf7,\xd7\xa2\xca\xcd '


# ***********************************************************************
class Point:
    def __init__(self, x, y, line=0):
        self.x = x
        self.y = y
        self.line = line


# ***********************************************************************
class Smd:
    smdParams = {
        # Pattern     height xOff yOff Feed Size
        "DIP4": [3.6, 0, 0, 12, 1],
        "TSSOP_20": [1.5, -9.55, 6.89, 12, 2],
        "LEDD": [0.78, 0.16, 0, 4, 0],
        "10X16": [3.6, 0, 0, 4, 1],
        "0805": [0.5, 0.7, 0, 4, 0],
        "1206": [0.5, 0.6, 0, 4, 0],
        "2512": [0.5, 0.6, 0, 4, 1],
        "SOD80_S": [1.5, 0.66, 0.16, 4, 0],  # BZV55C
        "SOT-23": [0.5, 0.75, 0.3, 4, 0],  # BAS40-06
        "SOT-223": [1.5, -9.2, 7.15, 4, 0],  # BAS40-06
        "DB-1S": [2.4, 0.22, -0.2, 12, 2],  # DB107S
        "K1010": [2.4, 0, 0, 8, 1],  # K1010
        "SM-6": [3.6, 8.07, -0.15, 12, 2],  # MOC3063
        "SO8": [1.5, 0.66, -0.28, 8, 1],  # PIC12F675
        "64A": [1.5, -4.7, 2.5, 4, 2],  # 64A
        "ATMEGA8": [1.5, -4.7, 2.5, 4, 2],  # ATMEGA8
        "SOD323": [0.5, 0.7, 0, 4, 0],
        "LED_0805": [0.5, 0.7, 0, 4, 0],
        "MB8S": [2.4, 0.7, 0, 8, 1]

    }

    @staticmethod
    def get_height(pattern_name):
        return Smd.smdParams[pattern_name][0]

    @staticmethod
    def get_x_offset(pattern_name):
        return Smd.smdParams[pattern_name][1]

    @staticmethod
    def get_y_offset(pattern_name):
        return Smd.smdParams[pattern_name][2]

    @staticmethod
    def get_feed_rate(pattern_name):
        return Smd.smdParams[pattern_name][3]

    @staticmethod
    def get_size_type(pattern_name):
        return Smd.smdParams[pattern_name][4]

    def __init__(self, number, pattern_name, value):
        self.number = number
        self.value = value
        self.pattern_name = pattern_name
        try:
            self.height = self.get_height(pattern_name)
        except:
            self.height = 0


# ***********************************************************************
stacks = []


# ***********************************************************************
class Component:
    def __init__(self, center, angle, description, comp_type, pattern_name, value):
        self.center = center
        self.center.x = self.center.x * xCoef
        self.center.y = self.center.y * yCoef
        self.angle = 90 + angle
        if self.angle > 360:
            self.angle -= 360
        self.description = description
        self.pattern_name = pattern_name
        self.type = comp_type
        self.value = value
        self.onlyPaste = False
        self.skip = 0
        real_angle = angle
        if self.value == "400Kx2":
            self.value = "430K"
        if self.value == "BZV55C":
            self.value = "5V1"
        if self.value == "50K":
            self.value = "51K"
        if self.value == "Value":
            self.value = ""
        if self.value == "":
            self.value = self.type
        if self.value == " ":
            self.value = self.type
        if self.value == "NONE":
            self.value = self.type
        if self.value.find("3063") != -1:
            self.value = "3063"
        if self.value.find("3023") != -1:
            self.value = "3023"
        if self.description.find("LM358D") != -1:
            self.value = "2904"
        if self.value.find("LM358D") != -1:
            self.value = "2904"
        if self.pattern_name.find("1206") != -1:
            self.pattern_name = "1206"
        if self.pattern_name.find("R2512") != -1:
            self.pattern_name = "2512"
        if self.value.find("MOC30XX") != -1:
            self.value = "3023"
        if self.value.find("BZV55C") != -1:
            self.value = "5V1"
        if self.value.find("10X16") != -1:
            self.value = "10X16"
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if pattern_name == "SM-6":
            self.angle = angle
        if pattern_name == "SO8":
            self.angle = angle
        if pattern_name == "TSSOP_20":
            self.angle = angle
        if pattern_name == "SOT-23":
            self.angle = angle
        if pattern_name == "ATMEGA8":
            self.angle = angle
        if pattern_name == "DB-1S":
            self.value = "107"
            self.angle = self.angle + 180
        if (pattern_name.find("TLP521") != -1) or (value.find("TLP521") != -1) or \
                (description.find("TLP521") != -1) or (pattern_name.find("K1010") != -1) or \
                (value.find("K1010") != -1) or (description.find("K1010") != -1):
            self.pattern_name = "K1010"
            self.value = "K1010"
            self.angle = self.angle + 180
        if pattern_name == "TO-269AA":
            self.pattern_name = "MB8S"
            self.value = "MB8S"
            self.angle = self.angle + 270
            real_angle = real_angle + 270
        if self.angle >= 360:
            self.angle -= 360
        if pattern_name == "0805" and self.value == "3K":
            self.type = "R0805"
        if self.value.find("40-06") != -1:
            self.value = "4006"
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # if(self.value.find("MOC") >= 0):
        #    self.value = ""
        # self.description = self.value
        self.error = True
        self.stack = 0
        self.height = 0.5
        self.sizeType = Smd.get_size_type(self.pattern_name)

        for st in stacks:
            st_value = st.value
            self.onlyPaste = False
            self.skip = 0
            if st_value.find("*") != -1:
                self.onlyPaste = True
                self.skip = 1
                st_value = st_value.replace("*", "")
            if self.pattern_name == st.pattern_name and st.number != 0 and self.value == st_value:  # or\
                # ((self.type != "R1206") & (self.type != "R0805") & (self.type != "C0805")):
                self.stack = st.number
                self.height = st.height
                self.error = False
                break

        if not self.error:
            self.pins = []
            if self.pattern_name == "0805":
                self.pins.append(Point(-2.21 / 2, 0, DOT_SMALL))
                self.pins.append(Point(2.21 / 2, 0, DOT_SMALL))
                if self.angle > 90:
                    self.angle -= 180
            if self.pattern_name == "1206":
                self.pins.append(Point(-3.25 / 2, 0, DOT_MEDIUM))
                self.pins.append(Point(3.25 / 2, 0, DOT_MEDIUM))
                if self.angle > 90:
                    self.angle -= 180
            if self.pattern_name == "2512":
                self.pins.append(Point(-3, 0, DOT_BIG))
                self.pins.append(Point(3, 0, DOT_BIG))
                self.pins.append(Point(-3, 1, DOT_BIG))
                self.pins.append(Point(3, 1, DOT_BIG))
                self.pins.append(Point(-3, -1, DOT_BIG))
                self.pins.append(Point(3, -1, DOT_BIG))
                if self.angle > 90:
                    self.angle -= 180
            if (ignoreRotation and (self.angle <= 90)) or not ignoreRotation:
                if (self.pattern_name == "SOD323") or (self.pattern_name == "LED_0805"):
                    self.pins.append(Point(-2.21 / 2, 0, DOT_SMALL))
                    self.pins.append(Point(2.21 / 2, 0, DOT_SMALL))
                if self.pattern_name == "10X16":
                    self.pins.append(Point(-1.7, 0, DOT_MEDIUM))
                    self.pins.append(Point(1.7, 0, DOT_MEDIUM))
                    self.pins.append(Point(-3, 0, DOT_MEDIUM))
                    self.pins.append(Point(3, 0, DOT_MEDIUM))
                    if self.value == "22X16":
                        self.pins.append(Point(-4.5, 0, DOT_BIG))
                        self.pins.append(Point(4.5, 0, DOT_BIG))
                    self.angle += 180
                    if self.angle >= 360:
                        self.angle -= 360
                if self.pattern_name == "LEDD":
                    self.pins.append(Point(-1, 0, DOT_SMALL))
                    self.pins.append(Point(1, 0, DOT_SMALL))
                    if self.angle > 90:
                        self.angle -= 180
                if self.pattern_name == "SOT-23":
                    self.pins.append(Point(-2.47 / 2, -1.80 / 2, DOT_SMALL))
                    self.pins.append(Point(2.47 / 2, -1.80 / 2, DOT_SMALL))
                    self.pins.append(Point(0, 2.47 / 2, DOT_SMALL))
                if self.pattern_name == "SOD80_S":
                    self.pins.append(Point(-2.2, 0, DOT_BIG))
                    self.pins.append(Point(-1.20, 0, DOT_MEDIUM))
                    self.pins.append(Point(1.60, 0, DOT_MEDIUM))
                    self.pins.append(Point(2.5, 0, DOT_BIG))
                if self.pattern_name == "DB-1S":
                    self.pins.append(Point(4.20, -2.70, DOT_MEDIUM))
                    self.pins.append(Point(4.20, 2.70, DOT_MEDIUM))
                    self.pins.append(Point(-4.20, -2.70, DOT_MEDIUM))
                    self.pins.append(Point(-4.20, 2.70, DOT_MEDIUM))
                    self.pins.append(Point(5.40, -2.70, DOT_MEDIUM))
                    self.pins.append(Point(5.40, 2.70, DOT_MEDIUM))
                    self.pins.append(Point(-5.40, -2.70, DOT_MEDIUM))
                    self.pins.append(Point(-5.40, 2.70, DOT_MEDIUM))
                if self.pattern_name == "MB8S":
                    self.pins.append(Point(3, -1.20, DOT_BIG))
                    self.pins.append(Point(3, 1.20, DOT_BIG))
                    self.pins.append(Point(-3, -1.20, DOT_BIG))
                    self.pins.append(Point(-3, 1.20, DOT_BIG))
                if self.pattern_name == "K1010":
                    self.pins.append(Point(4, -1.25, DOT_MEDIUM))
                    self.pins.append(Point(4, 1.25, DOT_MEDIUM))
                    self.pins.append(Point(4.5, -1.25, DOT_MEDIUM))
                    self.pins.append(Point(4.5, 1.25, DOT_MEDIUM))
                    self.pins.append(Point(-4, -1.25, DOT_MEDIUM))
                    self.pins.append(Point(-4, 1.25, DOT_MEDIUM))
                    self.pins.append(Point(-4.5, -1.25, DOT_MEDIUM))
                    self.pins.append(Point(-4.5, 1.25, DOT_MEDIUM))
                if self.pattern_name == "DIP4":
                    self.pins.append(Point(4.20, -1.2, DOT_MEDIUM))
                    self.pins.append(Point(4.20, 1.2, DOT_MEDIUM))
                    self.pins.append(Point(-4.20, -1.2, DOT_MEDIUM))
                    self.pins.append(Point(-4.20, 1.2, DOT_MEDIUM))
                if self.pattern_name == "SM-6":
                    self.pins.append(Point(4.62, -2.36, DOT_BIG))
                    self.pins.append(Point(4.62, 2.36, DOT_BIG))
                    self.pins.append(Point(-4.64, -0.17, DOT_BIG))
                    self.pins.append(Point(-4.64, 2.36, DOT_BIG))
                if self.pattern_name == "SO8":
                    self.pins.append(Point(-3.1, 1.90, DOT_SMALL))
                    self.pins.append(Point(-3.1, 0.63, DOT_SMALL))
                    self.pins.append(Point(-3.1, -0.63, DOT_SMALL))
                    self.pins.append(Point(-3.1, -1.90, DOT_SMALL))
                    self.pins.append(Point(3.1, 1.90, DOT_SMALL))
                    self.pins.append(Point(3.1, 0.63, DOT_SMALL))
                    self.pins.append(Point(3.1, -0.63, DOT_SMALL))
                    self.pins.append(Point(3.1, -1.90, DOT_SMALL))
                if self.pattern_name == "TSSOP_20":
                    self.pins.append(Point(-2.8, 3.10, DOT_SMALL))
                    self.pins.append(Point(-2.8, -3.10, DOT_SMALL))
                    self.pins.append(Point(2.8, 3.10, DOT_SMALL))
                    self.pins.append(Point(2.8, -3.10, DOT_SMALL))
                if self.pattern_name == "SOT-223":
                    self.pins.append(Point(-2.3, -3, DOT_MEDIUM))
                    self.pins.append(Point(0, -3, DOT_MEDIUM))
                    self.pins.append(Point(2.3, -3, DOT_MEDIUM))
                    self.pins.append(Point(0, 3, DOT_MEDIUM))
                if self.pattern_name == "64A":  # lNog=12.4, half=6.2; lCorp=15.4, half=7.7
                    self.pins.append(Point(-5.2, -7.7, DOT_MEDIUM))
                    self.pins.append(Point(-3.2, -7.7, DOT_MEDIUM))
                    self.pins.append(Point(-1.2, -7.7, DOT_MEDIUM))
                    self.pins.append(Point(1.2, -7.7, DOT_MEDIUM))
                    self.pins.append(Point(3.2, -7.7, DOT_MEDIUM))
                    self.pins.append(Point(5.2, -7.7, DOT_MEDIUM))
                    self.pins.append(Point(-5.2, 7.7, DOT_MEDIUM))
                    self.pins.append(Point(-3.2, 7.7, DOT_MEDIUM))
                    self.pins.append(Point(-1.2, 7.7, DOT_MEDIUM))
                    self.pins.append(Point(1.2, 7.7, DOT_MEDIUM))
                    self.pins.append(Point(3.2, 7.7, DOT_MEDIUM))
                    self.pins.append(Point(5.2, 7.7, DOT_MEDIUM))
                    self.pins.append(Point(-7.7, -5.2, DOT_MEDIUM))
                    self.pins.append(Point(-7.7, -3.2, DOT_MEDIUM))
                    self.pins.append(Point(-7.7, -1.2, DOT_MEDIUM))
                    self.pins.append(Point(-7.7, 1.2, DOT_MEDIUM))
                    self.pins.append(Point(-7.7, 3.2, DOT_MEDIUM))
                    self.pins.append(Point(-7.7, 5.2, DOT_MEDIUM))
                    self.pins.append(Point(7.7, -5.2, DOT_MEDIUM))
                    self.pins.append(Point(7.7, -3.2, DOT_MEDIUM))
                    self.pins.append(Point(7.7, -1.2, DOT_MEDIUM))
                    self.pins.append(Point(7.7, 1.2, DOT_MEDIUM))
                    self.pins.append(Point(7.7, 3.2, DOT_MEDIUM))
                    self.pins.append(Point(7.7, 5.2, DOT_MEDIUM))
                if self.pattern_name == "ATMEGA8":  # lNog=6.2, half=3.1; lCorp=9.2, half=4.6
                    self.pins.append(Point(-3.05, 4.6, DOT_SMALL))
                    self.pins.append(Point(-1.05, 4.6, DOT_SMALL))
                    self.pins.append(Point(1.05, 4.6, DOT_SMALL))
                    self.pins.append(Point(3.05, 4.6, DOT_SMALL))
                    self.pins.append(Point(-3.05, -4.6, DOT_SMALL))
                    self.pins.append(Point(-1.05, -4.6, DOT_SMALL))
                    self.pins.append(Point(1.05, -4.6, DOT_SMALL))
                    self.pins.append(Point(3.05, -4.6, DOT_SMALL))
                    self.pins.append(Point(4.6, -3.05, DOT_SMALL))
                    self.pins.append(Point(4.6, -1.05, DOT_SMALL))
                    self.pins.append(Point(4.6, 1.05, DOT_SMALL))
                    self.pins.append(Point(4.6, 3.05, DOT_SMALL))
                    self.pins.append(Point(-4.6, -3.05, DOT_SMALL))
                    self.pins.append(Point(-4.6, -1.05, DOT_SMALL))
                    self.pins.append(Point(-4.6, 1.05, DOT_SMALL))
                    self.pins.append(Point(-4.6, 3.05, DOT_SMALL))

            if self.angle < 0:
                self.angle += 360
            if len(self.pins) == 0:
                self.error = True
            else:
                for pin in self.pins:
                    xz = self.center.x + pin.x * math.cos(real_angle * PI / 180) - \
                        pin.y * math.sin(real_angle * PI / 180)
                    yz = self.center.y + pin.x * math.sin(real_angle * PI / 180) + \
                        pin.y * math.cos(real_angle * PI / 180)
                    pin.x = xz
                    pin.y = yz


# Глобальные настройки
Window.size = (1400, 700)
Window.top = 100
Window.left = 100
Window.clear_color = (255 / 255, 186 / 255, 3 / 255, 1)
Window.title = "Solder Paste"


class Container(BoxLayout):
    ti_size_x = ObjectProperty()
    ti_size_y = ObjectProperty()
    ti_devices_number_x = ObjectProperty()
    ti_devices_number_y = ObjectProperty()
    ti_name = ObjectProperty()
    cb_chart = ObjectProperty()
    cb_sd_chmt = ObjectProperty()
    cb_sd_dispenser = ObjectProperty()
    bl_coils = ObjectProperty()
    ll_out = ObjectProperty()
    b_input_pcad = ObjectProperty()
    b_input_saved = ObjectProperty()

    def print_custom(self, text, end="\n"):
        self.ll_out.text += text + end
        pass

    def input_pcad(self):
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
        file_input = pathToFolder + "Input.txt"
        file_out = open(file_input, 'w')
        input_text = pyperclip.paste()
        input_text = input_text.replace('\n', '')
        print(input_text)
        file_out.write(input_text)
        file_out.close()

    def correct_coords(self):
        point = pathToFolder.rfind("\\")
        this_directory = pathToFolder[:point]
        point = this_directory.rfind("\\")
        this_directory = pathToFolder[:point]
        error = False
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Correct file", ".csv")])
        point = file_path.rfind("/") + 1
        input_file_name = file_path[point:]
        input_file_name = input_file_name.replace(".csv", "")
        input_file = file_path
        files = os.listdir(this_directory)
        main_file_path = ""
        for f in files:
            if f.find(".csv") != -1:
                f = f.replace(".csv", "")
                if input_file_name.find(f) != -1:
                    main_file_path = this_directory + "\\" + f + ".csv"
                    break
        else:
            print("Нет файла импорта")
            input_file = ""

        if input_file != "":
            fin = open(input_file, 'r')
            print("Калибровочный файл: ", input_file)
            self.print_custom("Калибровочный файл: " + input_file)
            file_main = open(main_file_path, 'r')
            print("Основной файл: ", main_file_path)
            self.print_custom("Основной файл: " + main_file_path)
            # ============================================================
            start_decode = False
            block_number = 0
            strings = []
            str_blocks = ""
            for strFile in fin:
                if start_decode:
                    str_blocks = str_blocks + strFile
                else:
                    if strFile.find("%") != -1:
                        block_number += 1
                        if block_number == 4:
                            start_decode = True
                    continue
            strings = str_blocks.split("\n")
            # print(strings)
            arr_coords = []
            for st in strings:
                pos_start = 0
                for i in range(3):
                    pos_start = st.find(",", pos_start) + 1
                pos_end = pos_start
                for i in range(2):
                    pos_end = st.find(",", pos_end) + 1
                coords = st[pos_start:pos_end - 1]
                pos_start = st.find(",", pos_end) + 1
                for i in range(3):
                    pos_start = st.find(",", pos_start) + 1
                pos_end = st.find(",", pos_start)
                des_def = st[pos_start + 1:pos_end]
                des_def = des_def.split(" ")[0]
                data = coords.split(",")
                data.append(des_def)
                arr_coords.append(data)
            arr_coords.pop()
            fin.close()
            # ============================================================
            start_decode = False
            block_number = 0
            strings = []
            str_blocks = ""
            for strFile in file_main:
                if start_decode:
                    str_blocks = str_blocks + strFile
                else:
                    if strFile.find("%") != -1:
                        block_number += 1
                        if block_number == 4:
                            start_decode = True
                    continue
            strings = str_blocks.split("\n")
            # print(strings)
            arr_coords_main = []
            for st in strings:
                pos_start = 0
                for i in range(3):
                    pos_start = st.find(",", pos_start) + 1
                pos_end = pos_start
                for i in range(2):
                    pos_end = st.find(",", pos_end) + 1
                coords = st[pos_start:pos_end - 1]
                pos_start = st.find(",", pos_end) + 1
                for i in range(3):
                    pos_start = st.find(",", pos_start) + 1
                pos_end = st.find(",", pos_start)
                des_def = st[pos_start + 1:pos_end]
                des_def = des_def.split(" ")[0]
                data = coords.split(",")
                data.append(des_def)
                arr_coords_main.append(data)
            arr_coords_main.pop()
            # ============================================================
            for i in range(len(arr_coords)):
                diff_x = round(float(arr_coords[i][0]) - float(arr_coords_main[i][0]), 3)
                diff_y = round(float(arr_coords[i][1]) - float(arr_coords_main[i][1]), 3)
                arr_coords[i][0] = str(diff_x)
                arr_coords[i][1] = str(diff_y)
                if (diff_x == 0) and (diff_y == 0):
                    arr_coords[i][2] = "none"
                # print(f'{i + 1}: {arr_coords[i]}')
            file_main.close()
            # ============================================================
            if not error:
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
                file_input = pathToFolder + "Input.txt"
                file_out = open(file_input, 'w')
                input_text = pyperclip.paste()
                input_text = input_text.replace('\n', '')
                # print(input_text)
                file_out.write(input_text)
                file_out.close()

    def input_saved(self):
        global device_name
        global size_x
        global size_y
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Input files", ".txt")])
        # D:/Programs/For_Work/Dev-Cpp/devcpp.exe
        if file_path.find("input") != -1:
            file_name = file_path.split("/")[-1]
            pos = file_name.rfind(".")
            file_name = file_name[:pos]
            device_params = file_name.split("input")
            device_name = device_params[0]
            coords = device_params[1].split("x")
            size_x = float(coords[0])
            size_y = float(coords[1])
            self.ti_name.text = device_name
            self.ti_size_x.text = str(size_x)
            self.ti_size_y.text = str(size_y)
            shutil.copy(file_path, pathToFolder + "Input.txt")
        pass

    def raschet(self):
        self.print_custom("\n")
        if True:
            file_name = "input.txt"
            # global file_name
            global split_size_type
            global device_name
            global size_x
            global size_y
            global devices_number_x
            global devices_number_y
            global showPlot
            global copyToSdChmt
            global copyToSddispenser
            global pathToFolder
            global stackError
            global coils
            self.ll_out.text = ""
            device_name = self.ti_name.text
            size_x = float(self.ti_size_x.text)
            size_y = float(self.ti_size_y.text)
            devices_number_x = int(self.ti_devices_number_x.text)
            devices_number_y = int(self.ti_devices_number_y.text)
            if self.cb_chart.active:
                showPlot = True
            else:
                showPlot = False
            if self.cb_sd_chmt.active:
                copyToSdChmt = True
            else:
                copyToSdChmt = False
            if self.cb_sd_dispenser.active:
                copyToSddispenser = True
            else:
                copyToSddispenser = False
            if self.cbSplitSize.active:
                split_size_type = True
            else:
                split_size_type = False
            path_to_file = pathToFolder + file_name
            if devices_number_x == 0:
                devices_number_x = 1
            if devices_number_y == 0:
                devices_number_y = 1
            # print(self.ids)
            for kat in range(KOLVO_KATUSHEK):
                coils[kat] = self.ids[str("kat" + str(kat + 1))].text
                katushka = coils[kat].split()
                if len(katushka) == 2:
                    stacks[kat].value = katushka[1]
                    stacks[kat].pattern_name = katushka[0]
                    try:
                        self.height = self.getHeight(stacks[kat].pattern_name)
                    except:
                        self.height = 0

            # --------------------------------------------------------------
            split_count = 1
            if split_size_type:
                split_count = 2
            for split_file in range(split_count):
                fin = open(path_to_file, 'r')
                if split_file:
                    size_type_small = True
                else:
                    size_type_small = False
                # Write
                if split_size_type:
                    if size_type_small:
                        mark_file = "s"
                    else:
                        mark_file = "b"
                else:
                    mark_file = ""
                file_chmt_name = pathToFolderOutput + device_name + mark_file + ".csv"
                file_out = open(file_chmt_name, 'w')
                # ---------------------- Origin offset ----------------------
                file_out.close()
                file_out = open(file_chmt_name, 'ab')
                # FIRST_STRING = b'\x25\x2c\xd4\xad\xb5\xe3\xc6\xab\xd2\xc6'
                file_out.write(FIRST_STRING)
                file_out.close()
                file_out = open(file_chmt_name, 'a')
                file_out.write("\n")
                file_out.write("65535,0,")
                file_out.write("0")
                file_out.write(",")
                file_out.write("0")
                file_out.write(",")
                file_out.write("0")
                file_out.write(",")
                file_out.write("0")
                #    file_out.write(str(size_x))
                #    file_out.write(",")
                #    file_out.write(str(size_y))
                #    file_out.write(",")
                #    file_out.write(str(devices_number_x))
                #    file_out.write(",")
                #    file_out.write(str(devices_number_y))
                file_out.write("\n\n")
                # ---------------------- List of stacks ----------------------
                # c1cfd5bbc6abd2c6
                file_out.close()
                file_out = open(file_chmt_name, 'ab')
                # SECOND_STRING = b'\x25\x2c\xc1\xcf\xd5\xbb\xc6\xab\xd2\xc6'
                file_out.write(SECOND_STRING)
                file_out.close()
                file_out = open(file_chmt_name, 'a')
                file_out.write("\n")
                feed_rate = 2
                for kat in stacks:
                    if (kat.number != 0) and (kat.pattern_name != " "):
                        file_out.write("65535,1,")
                        file_out.write(str(kat.number))
                        file_out.write(",")
                        x_offset = Smd.get_x_offset(kat.pattern_name)
                        file_out.write(str(x_offset))
                        file_out.write(",")
                        y_offset = Smd.get_y_offset(kat.pattern_name)
                        file_out.write(str(y_offset))
                        file_out.write(",")
                        feed_rate = Smd.get_feed_rate(kat.pattern_name)
                        file_out.write(str(feed_rate))
                        file_out.write(".00,\"")
                        file_out.write(kat.pattern_name)
                        if kat.value != "":
                            file_out.write(" (")
                            file_out.write(kat.value)
                            file_out.write(")")
                        file_out.write("\",")
                        file_out.write("\n")
                file_out.write("\n")
                # ---------------------- List of PCB ----------------------
                # c6b4b0e5312c58
                file_out.close()
                file_out = open(file_chmt_name, 'ab')
                # THIRD_STRING = b'\x25\x2c\xc6\xb4\xb0\xe5\x31\x2c\x58'
                file_out.write(THIRD_STRING)
                file_out.close()
                file_out = open(file_chmt_name, 'a')
                file_out.write("\n")
                file_out.write("65535,")
                if size_x * size_y == 1:
                    file_out.write(str(3))
                else:
                    file_out.write(str(4))
                file_out.write(",")
                file_out.write(f"{size_x},{size_y},")
                file_out.write(f"{devices_number_x},{devices_number_y}\n\n")
                # ---------------------- List of components ----------------------
                # ccf9cdb7bac5
                file_out.close()
                file_out = open(file_chmt_name, 'ab')
                # FOURTH_STRING = b'\x25\x2c\xcc\xf9\xcd\xb7\xba\xc5'
                file_out.write(FOURTH_STRING)
                file_out.close()
                file_out = open(file_chmt_name, 'a')
                file_out.write("\n")
                # ----------------------------------------------------------------
                number = 0
                number_auto = 0
                number_decline = 0
                head = 0
                stack = 0
                value = ""
                x = 0
                y = 0
                angle = 0
                height = 0.5
                speed = 100
                head = 1
                stack = 1

                def print_pretty_table(data, cell_sep=' | ', header_separator=True):
                    rows = len(data)
                    cols = len(data[0])

                    col_width = []
                    for col in range(cols):
                        columns = [data[row][col] for row in range(rows)]
                        col_width.append(len(max(columns, key=len)))

                    separator = "-+-".join('-' * n for n in col_width)

                    for i, row in enumerate(range(rows)):
                        if i == 1 and header_separator:
                            self.print_custom(separator)

                        result = []
                        for col in range(cols):
                            item = data[row][col].rjust(col_width[col])
                            result.append(item)

                        self.print_custom(cell_sep.join(result))

                table_data = [
                    ['error', 'number', 'head', 'stack', 'x', 'y', 'angle', 'h', '0', 'type', 'description', 'speed']
                ]
                components = []
                components_fail = []
                # self.PrintCustom("k")
                searching_start = 1
                searching_start_cnt = 0
                for strInput in fin:
                    if searching_start:
                        searching_start_cnt += 1
                        if searching_start_cnt >= 4:
                            searching_start = 0
                    else:
                        dummy = strInput
                        dummy = dummy.replace("\n", "")
                        properties = dummy.split("\",\"")
                        i = 0
                        # self.PrintCustom(properties)
                        for k in properties:
                            k = k.replace("\"", "")
                            k = k.replace(",", ".")
                            properties[i] = k
                            # self.PrintCustom(properties[i])
                            i += 1
                        float(x)
                        pos = 0
                        # RefDes,Name,Type,Value,Layer,X,Y,Rotation
                        description = properties[0]
                        prop_name = properties[1]
                        comment = properties[2]
                        value = properties[3]
                        prop_layer = properties[4]
                        x = float(properties[5])
                        y = float(properties[6])
                        angle = float(properties[7])
                        if value == "104":
                            value = "0.1"
                        if prop_name == "TSSOP-20":
                            prop_name = prop_name
                        if prop_name == "SO8":
                            prop_name = prop_name

                        cur_comp = Component(Point(x, y), angle, description, comment, prop_name, value)
                        if cur_comp.type == "BAS40-06":
                            kek = 1

                        bool_str = "True"
                        if not cur_comp.error:
                            bool_str = "False"
                        table_data.append([bool_str, str(number), str(head), str(cur_comp.stack),
                                           str(cur_comp.center.x), str(cur_comp.center.y),
                                           str(round(cur_comp.angle)), str(cur_comp.height),
                                           str(0), str(cur_comp.type), str(cur_comp.description), str(speed)])
                        found = False
                        number += 1
                        if not cur_comp.error:
                            components.append(cur_comp)
                            found = True
                            # Формирование кода для станка
                            number_auto += 1
                            # if(not self.root.ids[str("cbKat"+str(kat.number))].enabled):
                            #   flag = False
                            if not split_size_type:
                                if cur_comp.sizeType == 0:
                                    head = 2
                                else:
                                    head = 1
                            else:
                                # Не подходящие по размеру компоненты пропускаю.
                                if size_type_small:
                                    # Исключаю большие и чередую головки
                                    if cur_comp.sizeType > 0:
                                        cur_comp.skip = 1
                                    else:
                                        if head == 2:
                                            head = 1
                                        else:
                                            head = 2
                                else:
                                    # Исключаю маленькие и задаю головки
                                    if cur_comp.sizeType == 0:
                                        cur_comp.skip = 1
                                    else:
                                        if cur_comp.sizeType == 1:
                                            head = 2
                                        else:
                                            head = 1
                            real_angle = round(cur_comp.angle)
                            desc_str = cur_comp.value
                            if cur_comp.value != "":
                                desc_str = str(cur_comp.description) + " " + desc_str
                                desc_str += " "
                                desc_str += str(cur_comp.type)
                            else:
                                desc_str = cur_comp.type

                            # if(not cur_comp.onlyPaste):
                            out_x = cur_comp.center.x
                            out_y = cur_comp.center.y
                            file_out.write(
                                f'{number_auto},{head},{cur_comp.stack},{round(out_x, 3)},'
                                f'{round(out_y, 3)},{real_angle},{cur_comp.height},{cur_comp.skip},'
                                f'{speed},"{desc_str}","{cur_comp.description}"\n')

                            if cur_comp.center.x == 0.0:
                                self.print_custom(f'{cur_comp.type} - ошибка, х = 0')

                        if not found:
                            number_decline += 1
                            components_fail.append(cur_comp)
                file_out.close()
                fin.close()

                # self.PrintCustom("-------------------------------------------------------------------")
            # self.PrintCustom(f"Катушки:")
            for kat in stacks:
                if kat.number > 0:
                    if kat.value != "":
                        pass
                        # self.PrintCustom(f"Катушка №{kat.number} -\t{kat.pattern_name}, {kat.value}","")
                    else:
                        pass
                        # self.PrintCustom(f"Катушка №{kat.number} -\t{kat.pattern_name}","")
                    flag = 0
                    # self.PrintCustom("")
                    only_dot_flag = False
                    for com in components:
                        kat_value = kat.value
                        if kat_value.find("*") != -1:
                            kat_value = kat_value.replace("*", "")
                            only_dot_flag = True
                        if (com.pattern_name == kat.pattern_name) and (com.value == kat_value):
                            if not only_dot_flag:
                                flag = 1
                            else:
                                flag = 2
                            break
                    if flag == 0:
                        # self.PrintCustom(" - не используется")
                        self.ids["kat" + str(kat.number)].background_color = [0.7, 0, 0.1, 1]
                    if flag == 1:
                        # self.PrintCustom("")
                        self.ids["kat" + str(kat.number)].background_color = [0, 1, 0, 1]
                    if flag == 2:
                        # self.PrintCustom("Только паста")
                        self.ids["kat" + str(kat.number)].background_color = [0.7, 0.6, 0.1, 1]
                else:
                    if kat.value != "":
                        pass
                        # self.PrintCustom(f"Вручную -\t{kat.pattern_name}, {kat.value}")
                    else:
                        pass
                        # self.PrintCustom(f"Вручную -\t{kat.pattern_name}")
                    stackError = 2

            if stackError:
                self.print_custom("-------------------------------------------------------------------")
                if stackError == 1:
                    self.print_custom("-------------------- Есть катушки с номером 0 ---------------------")
                if stackError == 2:
                    self.print_custom("------------------ Есть элементы с ручной пайкой ------------------")
                self.print_custom("-------------------------------------------------------------------\n")

            # Container.PrintCustom_pretty_table(table_data)

            self.print_custom("-------------------------------")
            self.print_custom(f"Количество компонентов - {number}")
            self.print_custom(f"Количество компонентов автоматической пайки - {number_auto}")
            self.print_custom(f"Количество необработанных компонентов - {number_decline}:")
            i = 0
            type_unique = []
            value_unique = []
            for k in components_fail:
                allow_adding = False
                # self.PrintCustom("+++++++++++++++++++++++++")
                # self.PrintCustom(len(type_unique))
                if len(type_unique) == 0:
                    allow_adding = True
                else:
                    kk = 0
                    allow_adding = True
                    for kk in range(len(type_unique)):
                        if (k.type == type_unique[kk]) and (k.value == value_unique[kk]):
                            allow_adding = False
                # allow_adding = True
                if allow_adding:
                    type_unique.append(k.type)
                    value_unique.append(k.value)
                    i += 1
                    self.print_custom(f"{i}) {k.description}, {k.pattern_name}, {k.type}, {k.value}")

            self.print_custom("-------------------------------")
            # --------------------------------------------------------------

            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            drives_rem = []
            for root in drives:
                if win32file.GetDriveTypeW(root) == DRIVE_REMOVABLE:
                    drives_rem.append(root)
            if len(drives_rem) == 1:
                file_sd = drives_rem[0]
            # print(len(drives_rem))
            if copyToSdChmt:
                if len(drives_rem) == 1:
                    if not split_size_type:
                        shutil.copy(file_chmt_name, file_sd)
                    else:
                        file_chmt_name = pathToFolderOutput + device_name + "s" + ".csv"
                        shutil.copy(file_chmt_name, file_sd)
                        file_chmt_name = pathToFolderOutput + device_name + "b" + ".csv"
                        shutil.copy(file_chmt_name, file_sd)
                if len(drives_rem) == 0:
                    ctypes.windll.user32.MessageBoxW(0, u"Не найдена SD-карта!\nФайл не записан.", u"Ошибка", 0)
                if len(drives_rem) > 1:
                    ctypes.windll.user32.MessageBoxW(0, u"Найдено больше одной SD-карты, оставьте нужную!\nФайл не "
                                                        u"записан.", u"Ошибка", 0)

            if components:
                # ----- Подготовка файла для дозатора -----
                # ------------ Read PNP file --------------
                # --------------------------------------------------------------
                # Coord ged and mux coeff
                coords = []
                coords_save = []
                for com in components:
                    for coord in com.pins:
                        coords.append(coord)
                for com in coords:
                    coords_save.append(com)
                # --------------------------------------------------------------
                self.print_custom(f"Количество точек - {len(coords)}")
                self.print_custom("-------------------------------")
                # --------------------------------------------------------------
                coords_sort = []

                index_min = 0

                dot_min = Point(0, 0)
                len_min = 10000.0
                for i in range(0, len(coords) - 1):
                    lenq = math.sqrt(math.pow(coords[i].x, 2) + math.pow(coords[i].y, 2))
                    if (len_min == 0.0) or (len_min > lenq):
                        len_min = lenq
                        dot_min.x = coords[i].x
                        dot_min.y = coords[i].y
                        dot_min.line = coords[i].line
                        index_min = i

                self.print_custom(f"")

                dot = Point(dot_min.x, dot_min.y, dot_min.line)
                coords_sort.append(dot)
                coords.pop(index_min)
                # --------------------------------------------------------------
                cnt = 0
                while len(coords) > 0:
                    lenq = 0.0
                    min_len = 0.0
                    min_len_index = 0
                    for i in range(len(coords)):
                        # if(coords[i].line != LINE_END):
                        lenq = math.sqrt(math.pow((coords[i].x - coords_sort[-1].x), 2) +
                                         math.pow((coords[i].y - coords_sort[-1].y), 2))
                        if (min_len == 0) or (min_len > lenq):
                            min_len = lenq
                            min_len_index = i

                    qdot = Point(coords[min_len_index].x, coords[min_len_index].y, coords[min_len_index].line)
                    coords_sort.append(qdot)
                    coords.pop(min_len_index)
                    if qdot.line == LINE_START:
                        qdot = Point(coords[min_len_index].x, coords[min_len_index].y, coords[min_len_index].line)
                        coords_sort.append(qdot)
                        coords.pop(min_len_index)
                    else:
                        if qdot.line == LINE_END:
                            qdot = Point(coords[min_len_index - 1].x, coords[min_len_index - 1].y,
                                         coords[min_len_index - 1].line)
                            coords_sort.append(qdot)
                            coords.pop(min_len_index - 1)
                # --------------------------------------------------------------
                board_x = 0
                board_y = 0
                coordsNum = len(coords_sort)
                for board_x in range(devices_number_x):
                    for board_y in range(devices_number_y):
                        if (board_x > 0) or (board_y > 0):
                            for coord in range(coordsNum):
                                qdot = Point(coords_sort[coord].x + size_x * board_x,
                                             coords_sort[coord].y + size_y * board_y,
                                             coords_sort[coord].line)
                                coords_sort.append(qdot)
                # --------------------------------------------------------------
                if True:
                    dot_max = Point(0, 0)
                    len_max = 0.0
                    for i in range(0, len(coords_sort) - 1):
                        lenq = math.sqrt(math.pow(coords_sort[i].x, 2) + math.pow(coords_sort[i].y, 2))
                        if (len_max == 0.0) or (len_max < lenq):
                            len_max = lenq
                            dot_max.x = coords_sort[i].x
                            dot_max.y = coords_sort[i].y

                dot_max_b = Point(dot_max.x, dot_max.y - (devices_number_y - 1) * size_y)
                dot_max_t = Point(dot_min.x, dot_min.y + (devices_number_y - 1) * size_y)

                dot_min.x = dot_min.x * 100
                dot_min.y = dot_min.y * 100
                dot_max.x = dot_max.x * 100
                dot_max.y = dot_max.y * 100
                dot_max_t.x = dot_max_t.x * 100
                dot_max_t.y = dot_max_t.y * 100
                dot_max_b.x = dot_max_b.x * 100
                dot_max_b.y = dot_max_b.y * 100

                coords_cal = [dot_min, dot_max_t, dot_max, dot_max_b]
                # --------------------------------------------------------------
                file_name_control = pathToFolderOutput + device_name + "t.nc"
                file_out_control = open(file_name_control, 'w')
                file_out_control.write(";start control\n")
                file_out_control.write(f"d0:x{round(dot_min.x)}y{round(dot_min.y)}z0\n")
                file_out_control.write(f"d0:x{round(dot_max_t.x)}y{round(dot_max_t.y)}z0\n")
                file_out_control.write(f"d0:x{round(dot_max.x)}y{round(dot_max.y)}z0\n")
                file_out_control.write(f"d0:x{round(dot_max_b.x)}y{round(dot_max_b.y)}z0\n")
                file_out_control.write(f"d0:x0y0z0\n")
                file_out_control.write(";end\n")
                file_out_control.write(";m2")
                file_out_control.close()
                # --------------------------------------------------------------
                file_name_main = pathToFolderOutput + device_name + ".nc"
                file_code = open(file_name_main, 'w')
                # --------------------------------------------------------------
                file_code.write(";start\n")
                # --------------------------------------------------------------
                for i in range(len(coords_sort)):
                    coords_sort[i].x = (coords_sort[i].x * 100)
                    coords_sort[i].y = (coords_sort[i].y * 100)
                    if (coords_sort[i].line == LINE_START) or (coords_sort[i].line == LINE_END):
                        prefix = "l"
                    else:
                        prefix = "d" + str(coords_sort[i].line)
                    file_code.write(f"{prefix}:x{round(coords_sort[i].x)}y{round(coords_sort[i].y)}z0\n")
                    # self.PrintCustom(f"{prefix}:{coords_sort[i].x},{coords_sort[i].y}")
                # --------------------------------------------------------------
                file_code.write(f"d0:x0y0z0\n")
                file_code.write(";end\n")
                file_code.write(";m2")
                file_code.close()
                # --------------------------------------------------------------
                file_name = pathToFolderOutput + device_name + "x.nc"
                file_code = open(file_name, 'w')
                # --------------------------------------------------------------
                file_code.write(";start control\n")
                file_code.write(f"d0:x{round(dot_min.x)}y{round(dot_min.y)}z0\n")
                file_code.write(";end\n")
                file_code.write(";m2")
                file_code.close()
                # self.PrintCustom("-------------------------------")
                self.print_custom(f"Файл для станка CHM-T36:\n     {file_chmt_name}\n")
                self.print_custom(f"Файл для дозатора (калибровочный):\n     {file_name_control}\n")
                self.print_custom(f"Файл для дозатора (основной):\n     {file_name}")
                self.print_custom(f"Файл для дозатора (основной):\n     {file_name}")
                self.print_custom("-------------------------------")

                # --------------------------------------------------------------
                file_input_name = pathToFolderOutput + device_name + "input" + str(size_x) + "x" + str(size_y) + ".txt"
                file_input = pathToFolder + "input.txt"
                shutil.copy(file_input, file_input_name)
                # --------------------------------------------------------------
                if copyToSddispenser:
                    if len(drives_rem) == 1:
                        shutil.copy(file_name_control, file_sd)
                        shutil.copy(file_name_main, file_sd)
                        shutil.copy(file_name, file_sd)
                        shutil.copy(file_name, file_sd)
                    if len(drives_rem) == 0:
                        ctypes.windll.user32.MessageBoxW(0, u"Не найдена SD-карта!\nФайл не записан.", u"Ошибка", 0)
                    if len(drives_rem) > 1:
                        ctypes.windll.user32.MessageBoxW(0, u"Найдено больше одной SD-карты, оставьте нужную!\nФайл "
                                                            u"не записан.", u"Ошибка", 0)

                random.seed()

                if showPlot:
                    axes_x = []
                    axes_y = []
                    axes_xs = []
                    axes_ys = []
                    axes_xc = []
                    axes_yc = []
                    axes_xr = [0, 0]
                    axes_yr = [0, 0]
                    axes_xl = []
                    axes_yl = []
                    axes_t_xl = []
                    axes_t_yl = []
                    plt.ion()
                    for i in coords_sort:
                        if axes_xr[1] < i.x / 100:
                            axes_xr[1] = i.x / 100 + 5
                        if axes_yr[1] < i.y / 100:
                            axes_yr[1] = i.y / 100 + 5
                    for k in components:
                        if k.value != "":
                            plt.text(k.center.x - len(k.value) / 2, k.center.y + 0.5 + random.random(), k.value)
                        else:
                            plt.text(k.center.x - len(k.type) / 2, k.center.y + 0.5, k.type)
                        axes_xc.append(k.center.x)
                        axes_yc.append(k.center.y)
                    line_flag = False
                    for i in coords_cal:
                        axes_t_xl.append(i.x / 100)
                        axes_t_yl.append(i.y / 100)
                    for i in coords_save:
                        axes_xs.append(i.x)
                        axes_ys.append(i.y)
                    for i in coords_sort:
                        axes_x.append(i.x / 100)
                        axes_y.append(i.y / 100)
                        if True:
                            if i.line == 1:
                                line_flag = True
                                axes_xl.append(i.x / 100)
                                axes_yl.append(i.y / 100)
                            else:
                                if line_flag:
                                    line_flag = False
                                    axes_xl.append(i.x / 100)
                                    axes_yl.append(i.y / 100)
                    plt.plot(axes_x, axes_y, 'ro')
                    plt.plot(axes_xc, axes_yc, 'g+')
                    plt.plot(axes_t_xl, axes_t_yl, 'bs')
                    plt.axis('equal')
                    plt.draw()
                    # plt.pause(0.1)
                    plt.ioff()
                    plt.show()

            file_options_lines = [NUMBER_NAME + ") " + str(device_name), NUMBER_RAZMER_X + ") " + str(size_x),
                                  NUMBER_RAZMER_Y + ") " + str(size_y), NUMBER_KOLVO_X + ") " + str(devices_number_x),
                                  NUMBER_KOLVO_Y + ") " + str(devices_number_y),
                                  NUMBER_SHOW_PLOT + ") " + str(showPlot),
                                  NUMBER_SD_CHMT + ") " + str(copyToSdChmt),
                                  NUMBER_SD_dispenser + ") " + str(copyToSddispenser),
                                  NUMBER_SPLIT_SIZE + ") " + str(split_size_type)]
            for kat in range(KOLVO_KATUSHEK):
                file_options_lines.append("k" + str(kat + 1) + ") " + coils[kat])

            file_options = open(pathToFolder + "optionsSP.txt", 'w')
            for strInput in file_options_lines:
                file_options.write(strInput + "\n")
                # self.PrintCustom(strInput)
            file_options.close()
            # ***********************************************************************


class DisplayApp(App):

    # Создание всех виджетов (объектов)
    def __init__(self):
        super().__init__()

    def kek(self):
        print('ok')

    def on_start(self):
        global device_name
        global size_x
        global size_y
        global split_size_type
        global devices_number_x
        global devices_number_y
        global showPlot
        global copyToSdChmt
        global copyToSddispenser
        global pathToFolder
        global pathToFolderOutput
        global coils

        bl_kat_l = BoxLayout()
        bl_kat_l.orientation = "vertical"
        bl_kat_r = BoxLayout()
        bl_kat_r.orientation = "vertical"
        for kat in range(KOLVO_KATUSHEK):
            num = KOLVO_KATUSHEK - kat - 1
            bl_kat = BoxLayout()
            bl_kat.orientation = "horizontal"
            text_str = "№" + str(num + 1)
            if kat < KOLVO_LOTKOV:
                text_str = text_str + "(" + str(3 - kat) + ")"
            kat_label = Label(text=text_str)
            kat_text_input = TextInput(hint_text="1")
            kat_text_input.id = "kat" + str(num + 1)
            self.root.ids[kat_text_input.id] = kat_text_input
            kat_text_input.size_hint = (2, 1)
            kat_text_input.background_color = (1, 1, 0, 1)
            cb_enable = CheckBox(active=True)
            cb_enable.id = "enKat" + str(num + 1)
            cb_enable.color = (1, 0, 1, 1)
            bl_kat.add_widget(kat_label)
            # bl_kat.add_widget(cb_enable)
            bl_kat.add_widget(kat_text_input)
            if num % 2:
                bl_kat_r.add_widget(bl_kat)
            else:
                bl_kat_l.add_widget(bl_kat)
        kat_text_input = TextInput(hint_text="1")
        kat_text_input.id = "kat"
        self.root.bl_coils.orientation = "horizontal"
        self.root.bl_coils.add_widget(bl_kat_l)
        self.root.bl_coils.add_widget(bl_kat_r)

        last_slash = pathToFolder.rfind("\\")
        pathToFolder = pathToFolder[:last_slash + 1]
        pathToFolderOutput = pathToFolder[:-1]
        last_slash = pathToFolderOutput.rfind("\\")
        pathToFolderOutput = pathToFolder[:last_slash + 1]
        # Read
        path_to_file = pathToFolder + "optionsSP.txt"
        file_options = open(path_to_file, 'r')
        # Шаблон: х) параметр
        prev_i = 0
        file_options_lines = file_options.readlines()
        for strInput in file_options_lines:
            if strInput[0] == NUMBER_NAME:
                device_name = strInput[3:-1]
            if strInput[0] == NUMBER_RAZMER_X:
                size_x = float(strInput[3:-1])
            if strInput[0] == NUMBER_RAZMER_Y:
                size_y = float(strInput[3:-1])
            if strInput[0] == NUMBER_KOLVO_X:
                devices_number_x = int(strInput[3:-1])
            if strInput[0] == NUMBER_KOLVO_Y:
                devices_number_y = int(strInput[3:-1])
            if strInput[0] == NUMBER_SPLIT_SIZE:
                if strInput.find("False") != -1:
                    split_size_type = False
                else:
                    split_size_type = True
            if strInput[0] == NUMBER_SHOW_PLOT:
                if strInput.find("False") != -1:
                    showPlot = False
                else:
                    showPlot = True
            if strInput[0] == NUMBER_SD_CHMT:
                if strInput.find("False") != -1:
                    copyToSdChmt = False
                else:
                    copyToSdChmt = True
            if strInput[0] == NUMBER_SD_dispenser:
                if strInput.find("False") != -1:
                    copyToSddispenser = False
                else:
                    copyToSddispenser = True
            if strInput[0] == "k":
                pos = strInput.find(")")
                i = int(strInput[1:pos]) - 1
                if i > prev_i + 1:
                    j = prev_i + 1
                    while j < i:
                        smd_kat = Smd(j, " ", " ")
                        stacks.append(smd_kat)
                        j += 1
                prev_i = i
                coils[i] = strInput[pos + 2:-1]
                param_kat = coils[i].split()
                if len(param_kat) < 2:
                    param_kat = [" ", " "]
                smd_kat = Smd(i + 1, param_kat[0], param_kat[1])
                stacks.append(smd_kat)
                self.root.ids[str("kat" + str(i + 1))].text = coils[i]
        file_options.close()

        self.root.ti_name.text = device_name
        self.root.ti_size_x.text = str(size_x)
        self.root.ti_size_y.text = str(size_y)
        self.root.ti_devices_number_x.text = str(devices_number_x)
        self.root.ti_devices_number_y.text = str(devices_number_y)
        self.root.cb_chart.active = showPlot
        self.root.cb_sd_chmt.active = copyToSdChmt
        self.root.cb_sd_dispenser.active = copyToSddispenser
        self.root.cbSplitSize.active = split_size_type

        # print(self.root.ids)
        # self.root.ll_out.text = "sads"

    # Основной метод для построения программы
    def build(self):
        return Container()


# ***********************************************************************
# Запуск проекта
if __name__ == "__main__":
    DisplayApp().run()
# ***********************************************************************
press_key('esc')
# ***********************************************************************
