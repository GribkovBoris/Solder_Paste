# ==================================================================
import copy
import numpy as np
import shutil
import os
import weakref
import math
import matplotlib.pyplot as plt
import random
import os
import win32con
import win32api
import win32file
from time import sleep
from tkinter import *
from tkinter import messagebox as mb
import ctypes
import tkinter as tk
from tkinter import filedialog
# ---------------------------------------------------------------
import pyautogui
import sys
import time
import threading
import subprocess
from threading import Thread
from importlib import reload
import pyperclip
import traceback
from pynput.keyboard import Key, Listener, Controller
# ==================================================================
# Импорт всех классов
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
        timerExit = 0
        while (True):
            time.sleep(0.1)
            # print("ok")
            if (timerExit > 100):
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


def clickRight(coords, delay=0.01):
    x = coords.x
    y = coords.y
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
    time.sleep(delay)


def dblClick(coords, delay=0.01):
    x = coords.x
    y = coords.y
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(delay)


def clickDown(coords, delay=0.01):
    x = coords.x
    y = coords.y
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(delay)


def clickUp(coords, delay=0.01):
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
def PressKey(key, delay=0.01):
    pyautogui.press(key)
    if (delay > 0):
        time.sleep(delay)


def PressKeys(key1, key2, delay=0.01):
    hotkey(key1, key2)
    if (delay > 0):
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
NUMBER_SD_DOSATOR = "8"
NUMBER_SPLIT_SIZE = "9"
# LM358D - SO8 pic12f675
# 0.1 - 0.47
fileSd = "E:/"
allowConvert = 0
ignoreCoeff = 0
stackError = 0
coordCoef = 0.801
xCoef = 1.0
yCoef = 1.0
sizeTypeSmall = True
chmtXCoef = 1.0
chmtYCoef = 1.0
showPlot = False
copyToSdChmt = False
copyToSdDosator = False
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
deviceName = "test"
razmerX = 1
razmerY = 1
kolvoX = 1
kolvoY = 1
splitSizeType = False
showPlot = False
copyToSdChmt = False
copyToSdDosator = False
KOLVO_KATUSHEK = 32
KOLVO_LOTKOV = 3
katushki = [" "] * KOLVO_KATUSHEK
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
    def __init__(self, center, angle, description, type, pattern_name, value):
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
        if (pattern_name.find("TLP521") != -1) or (value.find("TLP521") != -1) or (description.find("TLP521") != -1) or \
                (pattern_name.find("K1010") != -1) or (value.find("K1010") != -1) or (description.find("K1010") != -1):
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
            comp_type = "R0805"
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
    tiRazmerX = ObjectProperty()
    tiRazmerY = ObjectProperty()
    tiKolvoX = ObjectProperty()
    tiKolvoY = ObjectProperty()
    tiName = ObjectProperty()
    cbGrafik = ObjectProperty()
    cbSdChmt = ObjectProperty()
    cbSdDosator = ObjectProperty()
    blKatushki = ObjectProperty()
    llOut = ObjectProperty()
    bInputPcad = ObjectProperty()
    bInputSaved = ObjectProperty()

    def print_custom(self, text, end="\n"):
        self.llOut.text += text + end
        pass

    def input_pcad(self):
        PressKeys('alt', 'tab', 0.8)
        PressKey('alt', 0.2)
        PressKey('right', 0.1)
        PressKey('enter', 0.1)
        for i in range(8):
            PressKey('down')
        PressKey('enter')
        for i in range(3):
            PressKey('tab')
        PressKey('enter')
        for i in range(2):
            PressKeys('shift', 'tab')
        for i in range(7):
            PressKey('down')
        PressKey('space')
        for i in range(8):
            PressKey('tab')
            if (i == 6) or (i == 5):
                PressKey('0')
        PressKey('down')
        PressKey('up')
        PressKey('tab')
        PressKey('tab')
        PressKey('space', 1.5)
        PressKey('alt')
        PressKey('right')
        PressKey('down')
        PressKey('up')
        PressKey('up')
        PressKey('enter')
        PressKey('alt')
        PressKey('right')
        PressKey('down')
        PressKey('down')
        PressKey('down')
        PressKey('enter')
        PressKeys('alt', 'f4', 0.2)
        PressKey('tab')
        PressKey('enter')
        PressKey('alt')
        PressKeys('alt', 'tab')
        file_input = pathToFolder + "Input.txt"
        fout = open(file_input, 'w')
        input_text = pyperclip.paste()
        input_text = input_text.replace('\n', '')
        print(input_text)
        fout.write(input_text)
        fout.close()

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
        main_file = ""
        for f in files:
            if f.find(".csv") != -1:
                f = f.replace(".csv", "")
                if input_file_name.find(f) != -1:
                    main_file = this_directory + "\\" + f + ".csv"
                    break
        else:
            print("Нет файла импорта")
            input_file = ""

        if (input_file != ""):
            fin = open(input_file, 'r')
            print("Калибровочный файл: ", input_file)
            self.print_custom("Калибровочный файл: " + input_file)
            fMain = open(main_file, 'r')
            print("Основной файл: ", main_file)
            self.print_custom("Основной файл: " + main_file)
            # ============================================================
            startDecode = False
            blockNumber = 0
            strings = []
            strBlocks = ""
            for strFile in fin:
                if (startDecode):
                    strBlocks = strBlocks + strFile
                else:
                    if (strFile.find("%") != -1):
                        blockNumber += 1
                        if (blockNumber == 4):
                            startDecode = True
                    continue
            strings = strBlocks.split("\n")
            # print(strings)
            arrCoords = []
            for st in strings:
                posStart = 0
                for i in range(3):
                    posStart = st.find(",", posStart) + 1
                posEnd = posStart
                for i in range(2):
                    posEnd = st.find(",", posEnd) + 1
                coords = st[posStart:posEnd - 1]
                posStart = st.find(",", posEnd) + 1
                for i in range(3):
                    posStart = st.find(",", posStart) + 1
                posEnd = st.find(",", posStart)
                desDef = st[posStart + 1:posEnd]
                desDef = desDef.split(" ")[0]
                data = coords.split(",")
                data.append(desDef)
                arrCoords.append(data)
            arrCoords.pop()
            fin.close()
            # ============================================================
            startDecode = False
            blockNumber = 0
            strings = []
            strBlocks = ""
            for strFile in fMain:
                if (startDecode):
                    strBlocks = strBlocks + strFile
                else:
                    if (strFile.find("%") != -1):
                        blockNumber += 1
                        if (blockNumber == 4):
                            startDecode = True
                    continue
            strings = strBlocks.split("\n")
            # print(strings)
            arrCoordsMain = []
            for st in strings:
                posStart = 0
                for i in range(3):
                    posStart = st.find(",", posStart) + 1
                posEnd = posStart
                for i in range(2):
                    posEnd = st.find(",", posEnd) + 1
                coords = st[posStart:posEnd - 1]
                posStart = st.find(",", posEnd) + 1
                for i in range(3):
                    posStart = st.find(",", posStart) + 1
                posEnd = st.find(",", posStart)
                desDef = st[posStart + 1:posEnd]
                desDef = desDef.split(" ")[0]
                data = coords.split(",")
                data.append(desDef)
                arrCoordsMain.append(data)
            arrCoordsMain.pop()
            # ============================================================
            for i in range(len(arrCoords)):
                diffX = round(float(arrCoords[i][0]) - float(arrCoordsMain[i][0]), 3)
                diffY = round(float(arrCoords[i][1]) - float(arrCoordsMain[i][1]), 3)
                arrCoords[i][0] = str(diffX)
                arrCoords[i][1] = str(diffY)
                if (diffX == 0) and (diffY == 0):
                    arrCoords[i][2] = "none"
                # print(f'{i + 1}: {arrCoords[i]}')
            fMain.close()
            # ============================================================
            if (not error):
                # numberComp = int(input("Количество компонентов в PCAD файле: "))
                pyautogui.keyDown('alt')
                time.sleep(0.1)
                pyautogui.keyDown('tab')
                time.sleep(0.3)
                pyautogui.keyDown('tab')
                time.sleep(0.1)
                pyautogui.keyUp('alt')
                time.sleep(0.1)
                PressKey('alt')
                for i in range(2):
                    PressKey('right')
                PressKey('enter')
                for i in range(4):
                    PressKey('up')
                PressKey('enter', 0.2)
                exitFlag = False
                number = 0
                prevRef = "NONE"
                while (not exitFlag):
                    # for i in range(7):
                    click(qPoint(x=839, y=366 - 40))  # scroll up
                    PressKey('home', 0.1)
                    time.sleep(0.1)
                    click(qPoint(x=882, y=366 - 40))  # select first ref
                    time.sleep(0.1)
                    pages = int(number / 15)  # 16 components in page
                    for i in range(pages):
                        PressKey('pagedown', 0.05)
                    numberLeft = number - pages * 15
                    for i in range(numberLeft):
                        PressKey('down', 0)
                    time.sleep(0.1)
                    click(qPoint(x=1025, y=370 - 40), 0.6)  # properties
                    click(qPoint(x=848, y=361 - 40), 0.1)  # ref
                    click(qPoint(x=848, y=361 - 40), 0.2)  # ref
                    PressKeys('ctrl', 'c', 0.1)
                    copiedRef = pyperclip.paste()
                    print(number, copiedRef)
                    if (copiedRef == prevRef):
                        exitFlag = True
                    else:
                        prevRef = copiedRef
                        for coords in arrCoords:
                            # print(coords[2])
                            if (copiedRef == coords[2]):
                                click(qPoint(x=1059, y=538), 0.05)  # x
                                click(qPoint(x=1059, y=538), 0.1)  # x
                                PressKeys('ctrl', 'x', 0.05)
                                copiedCoord = pyperclip.paste()
                                xNew = round(float(copiedCoord) + float(coords[0]), 3)
                                pyperclip.copy(str(xNew))
                                time.sleep(0.05)
                                PressKeys('ctrl', 'v', 0.2)
                                PressKey('tab')
                                PressKeys('ctrl', 'x', 0.05)
                                copiedCoord = pyperclip.paste()
                                yNew = round(float(copiedCoord) + float(coords[1]), 3)
                                pyperclip.copy(str(yNew))
                                time.sleep(0.05)
                                print("x: ", xNew, "y: ", yNew)
                                PressKeys('ctrl', 'v', 0.2)
                                PressKey('enter')
                                break
                        else:
                            PressKey('enter')
                        number += 1
                    # exitFlag = True#!1111111111111111111111111111111111111
                # PressKey('esc')
                for i in range(6):
                    PressKey('down')
                PressKey('enter', 0.1)
                # Reports
                if (True):
                    PressKey('alt', 0.2)
                    PressKey('right', 0.1)
                    PressKey('enter', 0.1)
                    for i in range(8):
                        PressKey('down')
                    PressKey('enter')
                    for i in range(3):
                        PressKey('tab')
                    PressKey('enter')
                    for i in range(2):
                        PressKeys('shift', 'tab')
                    for i in range(7):
                        PressKey('down')
                    PressKey('space')
                    for i in range(8):
                        PressKey('tab')
                        if (i == 6) or (i == 5):
                            PressKey('0')
                    PressKey('down')
                    PressKey('up')
                    PressKey('tab')
                    PressKey('tab')
                    PressKey('space', 1.5)
                    PressKey('alt')
                    PressKey('right')
                    PressKey('down')
                    PressKey('up')
                    PressKey('up')
                    PressKey('enter')
                    PressKey('alt')
                    PressKey('right')
                    PressKey('down')
                    PressKey('down')
                    PressKey('down')
                    PressKey('enter')
                    PressKeys('alt', 'f4', 0.2)
                    PressKey('tab')
                    PressKey('enter')
                    PressKey('alt')
                    PressKeys('alt', 'tab')
                    file_input = pathToFolder + "Input.txt"
                    fout = open(file_input, 'w')
                    input_text = pyperclip.paste()
                    input_text = input_text.replace('\n', '')
                    # print(input_text)
                    fout.write(input_text)
                    fout.close()

    def InputSaved(self):
        global deviceName
        global razmerX
        global razmerY
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Input files", ".txt")])
        # D:/Programs/For_Work/Dev-Cpp/devcpp.exe
        if (file_path.find("input") != -1):
            fileName = file_path.split("/")[-1]
            pos = fileName.rfind(".")
            fileName = fileName[:pos]
            deviceParams = fileName.split("input")
            deviceName = deviceParams[0]
            coords = deviceParams[1].split("x")
            razmerX = float(coords[0])
            razmerY = float(coords[1])
            self.tiName.text = deviceName
            self.tiRazmerX.text = str(razmerX)
            self.tiRazmerY.text = str(razmerY)
            shutil.copy(file_path, pathToFolder + "Input.txt")
        pass

    def Raschet(self):
        self.print_custom("\n")
        if True:
            fileName = "input.txt"
            # global fileName
            global splitSizeType
            global deviceName
            global razmerX
            global razmerY
            global kolvoX
            global kolvoY
            global showPlot
            global copyToSdChmt
            global copyToSdDosator
            global pathToFolder
            global stackError
            global katushki
            self.llOut.text = ""
            deviceName = self.tiName.text
            razmerX = float(self.tiRazmerX.text)
            razmerY = float(self.tiRazmerY.text)
            kolvoX = int(self.tiKolvoX.text)
            kolvoY = int(self.tiKolvoY.text)
            if (self.cbGrafik.active):
                showPlot = True
            else:
                showPlot = False
            if (self.cbSdChmt.active):
                copyToSdChmt = True
            else:
                copyToSdChmt = False
            if (self.cbSdDosator.active):
                copyToSdDosator = True
            else:
                copyToSdDosator = False
            if (self.cbSplitSize.active):
                splitSizeType = True
            else:
                splitSizeType = False
            pathToFile = pathToFolder + fileName
            if (kolvoX == 0):
                kolvoX = 1
            if (kolvoY == 0):
                kolvoY = 1
            allowConvert = 1
            # print(self.ids)
            for kat in range(KOLVO_KATUSHEK):
                katushki[kat] = self.ids[str("kat" + str(kat + 1))].text
                katushka = katushki[kat].split()
                if (len(katushka) == 2):
                    stacks[kat].value = katushka[1]
                    stacks[kat].pattern_name = katushka[0]
                    try:
                        self.height = self.getHeight(stacks[kat].pattern_name)
                    except:
                        self.height = 0

            # --------------------------------------------------------------
            splitCount = 1
            if (splitSizeType):
                splitCount = 2
            for splitFile in range(splitCount):
                fin = open(pathToFile, 'r')
                if (splitFile):
                    sizeTypeSmall = True
                else:
                    sizeTypeSmall = False
                # Write
                if (splitSizeType):
                    if (sizeTypeSmall):
                        markFile = "s"
                    else:
                        markFile = "b"
                else:
                    markFile = ""
                fileChmtName = pathToFolderOutput + deviceName + markFile + ".csv"
                fout = open(fileChmtName, 'w')
                # ---------------------- Origin offset ----------------------
                fout.close()
                fout = open(fileChmtName, 'ab')
                # FIRST_STRING = b'\x25\x2c\xd4\xad\xb5\xe3\xc6\xab\xd2\xc6'
                fout.write(FIRST_STRING)
                fout.close()
                fout = open(fileChmtName, 'a')
                fout.write("\n")
                fout.write("65535,0,")
                fout.write("0")
                fout.write(",")
                fout.write("0")
                fout.write(",")
                fout.write("0")
                fout.write(",")
                fout.write("0")
                if (False):
                    fout.write(str(razmerX))
                    fout.write(",")
                    fout.write(str(razmerY))
                    fout.write(",")
                    fout.write(str(kolvoX))
                    fout.write(",")
                    fout.write(str(kolvoY))
                fout.write("\n\n")
                # ---------------------- List of stacks ----------------------
                # c1cfd5bbc6abd2c6
                fout.close()
                fout = open(fileChmtName, 'ab')
                # SECOND_STRING = b'\x25\x2c\xc1\xcf\xd5\xbb\xc6\xab\xd2\xc6'
                fout.write(SECOND_STRING)
                fout.close()
                fout = open(fileChmtName, 'a')
                fout.write("\n")
                feedRate = 2
                for kat in stacks:
                    if ((kat.number != 0) and (kat.pattern_name != " ")):
                        fout.write("65535,1,")
                        fout.write(str(kat.number))
                        fout.write(",")
                        xOffset = Smd.get_x_offset(kat.pattern_name)
                        fout.write(str(xOffset))
                        fout.write(",")
                        yOffset = Smd.get_y_offset(kat.pattern_name)
                        fout.write(str(yOffset))
                        fout.write(",")
                        feedRate = Smd.get_feed_rate(kat.pattern_name)
                        fout.write(str(feedRate))
                        fout.write(".00,\"")
                        fout.write(kat.pattern_name)
                        if (kat.value != ""):
                            fout.write(" (")
                            fout.write(kat.value)
                            fout.write(")")
                        fout.write("\",")
                        fout.write("\n")
                fout.write("\n")
                # ---------------------- List of PCB ----------------------
                # c6b4b0e5312c58
                fout.close()
                fout = open(fileChmtName, 'ab')
                # THIRD_STRING = b'\x25\x2c\xc6\xb4\xb0\xe5\x31\x2c\x58'
                fout.write(THIRD_STRING)
                fout.close()
                fout = open(fileChmtName, 'a')
                fout.write("\n")
                fout.write("65535,")
                if (razmerX * razmerY == 1):
                    fout.write(str(3))
                else:
                    fout.write(str(4))
                fout.write(",")
                fout.write(f"{razmerX},{razmerY},")
                fout.write(f"{kolvoX},{kolvoY}\n\n")
                # ---------------------- List of components ----------------------
                # ccf9cdb7bac5
                fout.close()
                fout = open(fileChmtName, 'ab')
                # FOURTH_STRING = b'\x25\x2c\xcc\xf9\xcd\xb7\xba\xc5'
                fout.write(FOURTH_STRING)
                fout.close()
                fout = open(fileChmtName, 'a')
                fout.write("\n")
                # ----------------------------------------------------------------
                number = 0
                numberAuto = 0
                numberDecline = 0
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
                # table_data.append(['error', 'number', 'head', 'stack', 'x', 'y', 'angle', 'h', '0', 'type', 'description', 'speed'])
                components = []
                componentsFail = []
                # self.PrintCustom("k")
                searchingStart = 1
                searchingStartCnt = 0
                for strInput in fin:
                    if (searchingStart):
                        searchingStartCnt += 1
                        if (searchingStartCnt >= 4):
                            searchingStart = 0
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
                        pName = properties[1]
                        comment = properties[2]
                        value = properties[3]
                        pLayer = properties[4]
                        x = float(properties[5])
                        y = float(properties[6])
                        angle = float(properties[7])
                        if (value == "104"):
                            value = "0.1"
                        # self.PrintCustom("----------------------------------")
                        # self.PrintCustom(properties)
                        if (pName == "TSSOP-20"):
                            pName = pName
                        if (pName == "SO8"):
                            pName = pName

                        curComp = Component(Point(x, y), angle, description, comment, pName, value)
                        if (curComp.type == "BAS40-06"):
                            kek = 1

                        boolStr = "True"
                        if (curComp.error == False):
                            boolStr = "False"
                        table_data.append([boolStr, str(number), str(head), str(curComp.stack), str(curComp.center.x),
                                           str(curComp.center.y), str(round(curComp.angle)), str(curComp.height),
                                           str(0), str(curComp.type), str(curComp.description), str(speed)])
                        found = False
                        number += 1
                        if (curComp.error == False):
                            components.append(curComp)
                            found = True
                            # Формирование кода для станка
                            numberAuto += 1
                            # if(not self.root.ids[str("cbKat"+str(kat.number))].enabled):
                            #   flag = False
                            if (not splitSizeType):
                                if (curComp.sizeType == 0):
                                    head = 2
                                else:
                                    head = 1
                            else:
                                # Не подходящие по размеру компоненты пропускаю.
                                if (sizeTypeSmall):
                                    # Исключаю большие и чередую головки
                                    if (curComp.sizeType > 0):
                                        curComp.skip = 1
                                    else:
                                        if (head == 2):
                                            head = 1
                                        else:
                                            head = 2
                                else:
                                    # Исключаю маленькие и задаю головки
                                    if (curComp.sizeType == 0):
                                        curComp.skip = 1
                                    else:
                                        if (curComp.sizeType == 1):
                                            head = 2
                                        else:
                                            head = 1
                            real_angle = round(curComp.angle)
                            descStr = curComp.value
                            if (curComp.value != ""):
                                descStr = str(curComp.description) + " " + descStr
                                descStr += " "
                                descStr += str(curComp.type)
                            else:
                                descStr = curComp.type

                            # if(not curComp.onlyPaste):
                            outX = curComp.center.x
                            outY = curComp.center.y
                            fout.write(
                                f'{numberAuto},{head},{curComp.stack},{round(outX, 3)},{round(outY, 3)},{real_angle},{curComp.height},{curComp.skip},{speed},"{descStr}","{curComp.description}"\n')

                            if (curComp.center.x == 0.0):
                                self.print_custom(f'{curComp.type} - ошибка, х = 0')
                                # self.PrintCustom(f'{numberAuto},{head},{curComp.stack},{curComp.center.x},{curComp.center.y},{round(curComp.angle)},{curComp.height},0,"{curComp.type}","{curComp.description}",{speed}\n')

                        if (not found):
                            numberDecline += 1
                            componentsFail.append(curComp)
                fout.close()
                fin.close()

                # self.PrintCustom("-------------------------------------------------------------------")
            # self.PrintCustom(f"Катушки:")
            for kat in stacks:
                if (kat.number > 0):
                    if (kat.value != ""):
                        pass
                        # self.PrintCustom(f"Катушка №{kat.number} -\t{kat.pattern_name}, {kat.value}","")
                    else:
                        pass
                        # self.PrintCustom(f"Катушка №{kat.number} -\t{kat.pattern_name}","")
                    flag = 0
                    # self.PrintCustom("")
                    onlyDotFlag = False
                    for com in components:
                        katValue = kat.value
                        if (katValue.find("*") != -1):
                            katValue = katValue.replace("*", "")
                            onlyDotFlag = True
                        # self.PrintCustom(f"com.stack = {com.stack}, com.value = {com.value}, com.type = {com.type}, kat.type = {kat.type}")
                        if ((com.pattern_name == kat.pattern_name) and (com.value == katValue)):
                            if (not onlyDotFlag):
                                flag = 1
                            else:
                                flag = 2
                            break
                    if (flag == 0):
                        # self.PrintCustom(" - не используется")
                        self.ids["kat" + str(kat.number)].background_color = [0.7, 0, 0.1, 1]
                    if (flag == 1):
                        # self.PrintCustom("")
                        self.ids["kat" + str(kat.number)].background_color = [0, 1, 0, 1]
                    if (flag == 2):
                        # self.PrintCustom("Только паста")
                        self.ids["kat" + str(kat.number)].background_color = [0.7, 0.6, 0.1, 1]
                else:
                    if (kat.value != ""):
                        pass
                        # self.PrintCustom(f"Вручную -\t{kat.pattern_name}, {kat.value}")
                    else:
                        pass
                        # self.PrintCustom(f"Вручную -\t{kat.pattern_name}")
                    stackError = 2

            if (stackError):
                self.print_custom("-------------------------------------------------------------------")
                if (stackError == 1):
                    self.print_custom("-------------------- Есть катушки с номером 0 ---------------------")
                if (stackError == 2):
                    self.print_custom("------------------ Есть элементы с ручной пайкой ------------------")
                self.print_custom("-------------------------------------------------------------------\n")

            # Container.PrintCustom_pretty_table(table_data)

            self.print_custom("-------------------------------")
            self.print_custom(f"Количество компонентов - {number}")
            self.print_custom(f"Количество компонентов автоматической пайки - {numberAuto}")
            self.print_custom(f"Количество необработанных компонентов - {numberDecline}:")
            i = 0
            typeUnique = []
            valueUnique = []
            for k in componentsFail:
                allowAdding = False
                # self.PrintCustom("+++++++++++++++++++++++++")
                # self.PrintCustom(len(typeUnique))
                if (len(typeUnique) == 0):
                    allowAdding = True
                else:
                    kk = 0
                    allowAdding = True
                    for kk in range(len(typeUnique)):
                        if (k.type == typeUnique[kk]) and (k.value == valueUnique[kk]):
                            allowAdding = False
                # allowAdding = True
                if (allowAdding == True):
                    typeUnique.append(k.type)
                    valueUnique.append(k.value)
                    i += 1
                    self.print_custom(f"{i}) {k.description}, {k.pattern_name}, {k.type}, {k.value}")

            self.print_custom("-------------------------------")
            # --------------------------------------------------------------

            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            drivesRem = []
            for root in drives:
                if win32file.GetDriveTypeW(root) == DRIVE_REMOVABLE:
                    drivesRem.append(root)
            if (len(drivesRem) == 1):
                fileSd = drivesRem[0]
            # print(len(drivesRem))
            if (copyToSdChmt):
                if (len(drivesRem) == 1):
                    if (not splitSizeType):
                        shutil.copy(fileChmtName, fileSd)
                    else:
                        fileChmtName = pathToFolderOutput + deviceName + "s" + ".csv"
                        shutil.copy(fileChmtName, fileSd)
                        fileChmtName = pathToFolderOutput + deviceName + "b" + ".csv"
                        shutil.copy(fileChmtName, fileSd)
                if (len(drivesRem) == 0):
                    ctypes.windll.user32.MessageBoxW(0, u"Не найдена SD-карта!\nФайл не записан.", u"Ошибка", 0)
                if (len(drivesRem) > 1):
                    ctypes.windll.user32.MessageBoxW(0,
                                                     u"Найдено больше одной SD-карты, оставьте нужную!\nФайл не записан.",
                                                     u"Ошибка", 0)

            if (components):
                # MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
                # ----- Подготовка файла для дозатора -----
                # ------------ Read PNP file --------------
                # --------------------------------------------------------------
                # Coord ged and mux coeff
                coords = []
                coordsSave = []
                for com in components:
                    for coord in com.pins:
                        coords.append(coord)
                for com in coords:
                    coordsSave.append(com)
                # --------------------------------------------------------------
                self.print_custom(f"Количество точек - {len(coords)}")
                self.print_custom("-------------------------------")
                # --------------------------------------------------------------
                coordsSort = []

                indexMin = 0

                dotMin = Point(0, 0)
                lenMin = 10000.0
                for i in range(0, len(coords) - 1):
                    lenq = math.sqrt(math.pow((coords[i].x), 2) + math.pow((coords[i].y), 2))
                    if (lenMin == 0.0) or (lenMin > lenq):
                        lenMin = lenq
                        dotMin.x = coords[i].x
                        dotMin.y = coords[i].y
                        dotMin.line = coords[i].line
                        indexMin = i

                self.print_custom(f"")

                dot = Point(dotMin.x, dotMin.y, dotMin.line)
                coordsSort.append(dot)
                coords.pop(indexMin)
                # --------------------------------------------------------------
                cnt = 0
                while (len(coords) > 0):
                    lenq = 0.0
                    minLen = 0.0
                    minLenIndex = 0
                    for i in range(len(coords)):
                        # if(coords[i].line != LINE_END):
                        lenq = math.sqrt(math.pow((coords[i].x - coordsSort[-1].x), 2) + \
                                         math.pow((coords[i].y - coordsSort[-1].y), 2))
                        if ((minLen == 0) or (minLen > lenq)):
                            minLen = lenq
                            minLenIndex = i

                    qdot = Point(coords[minLenIndex].x, coords[minLenIndex].y, coords[minLenIndex].line)
                    coordsSort.append(qdot)
                    coords.pop(minLenIndex)
                    if (qdot.line == LINE_START):
                        qdot = Point(coords[minLenIndex].x, coords[minLenIndex].y, coords[minLenIndex].line)
                        coordsSort.append(qdot)
                        coords.pop(minLenIndex)
                    else:
                        if (qdot.line == LINE_END):
                            qdot = Point(coords[minLenIndex - 1].x, coords[minLenIndex - 1].y,
                                         coords[minLenIndex - 1].line)
                            coordsSort.append(qdot)
                            coords.pop(minLenIndex - 1)
                # --------------------------------------------------------------
                boardX = 0
                boardY = 0
                coordsNum = len(coordsSort)
                for boardX in range(kolvoX):
                    for boardY in range(kolvoY):
                        if ((boardX > 0) or (boardY > 0)):
                            for coord in range(coordsNum):
                                qdot = Point(coordsSort[coord].x + razmerX * boardX, \
                                             coordsSort[coord].y + razmerY * boardY, coordsSort[coord].line)
                                coordsSort.append(qdot)
                # --------------------------------------------------------------
                if (True):
                    dotMax = Point(0, 0)
                    lenMax = 0.0
                    for i in range(0, len(coordsSort) - 1):
                        lenq = math.sqrt(math.pow((coordsSort[i].x), 2) + math.pow((coordsSort[i].y), 2))
                        if (lenMax == 0.0) or (lenMax < lenq):
                            lenMax = lenq
                            dotMax.x = coordsSort[i].x
                            dotMax.y = coordsSort[i].y

                dotMaxB = Point(dotMax.x, dotMax.y - (kolvoY - 1) * razmerY)
                dotMinT = Point(dotMin.x, dotMin.y + (kolvoY - 1) * razmerY)

                dotMin.x = dotMin.x * 100
                dotMin.y = dotMin.y * 100
                dotMax.x = dotMax.x * 100
                dotMax.y = dotMax.y * 100
                dotMinT.x = dotMinT.x * 100
                dotMinT.y = dotMinT.y * 100
                dotMaxB.x = dotMaxB.x * 100
                dotMaxB.y = dotMaxB.y * 100

                coordsCal = []
                coordsCal.append(dotMin)
                coordsCal.append(dotMinT)
                coordsCal.append(dotMax)
                coordsCal.append(dotMaxB)
                # --------------------------------------------------------------
                fileNameControl = pathToFolderOutput + deviceName + "t.nc"
                foutControl = open(fileNameControl, 'w')
                foutControl.write(";start control\n")
                foutControl.write(f"d0:x{round(dotMin.x)}y{round(dotMin.y)}z0\n")
                foutControl.write(f"d0:x{round(dotMinT.x)}y{round(dotMinT.y)}z0\n")
                foutControl.write(f"d0:x{round(dotMax.x)}y{round(dotMax.y)}z0\n")
                foutControl.write(f"d0:x{round(dotMaxB.x)}y{round(dotMaxB.y)}z0\n")
                foutControl.write(f"d0:x0y0z0\n")
                foutControl.write(";end\n")
                foutControl.write(";m2")
                foutControl.close()
                # --------------------------------------------------------------
                fileNameMain = pathToFolderOutput + deviceName + ".nc"
                fCode = open(fileNameMain, 'w')
                # --------------------------------------------------------------
                fCode.write(";start\n")
                # --------------------------------------------------------------
                for i in range(len(coordsSort)):
                    coordsSort[i].x = (coordsSort[i].x * 100)
                    coordsSort[i].y = (coordsSort[i].y * 100)
                    if ((coordsSort[i].line == LINE_START) or (coordsSort[i].line == LINE_END)):
                        prefix = "l"
                    else:
                        prefix = "d" + str(coordsSort[i].line)
                    fCode.write(f"{prefix}:x{round(coordsSort[i].x)}y{round(coordsSort[i].y)}z0\n")
                    # self.PrintCustom(f"{prefix}:{coordsSort[i].x},{coordsSort[i].y}")
                # --------------------------------------------------------------
                fCode.write(f"d0:x0y0z0\n")
                fCode.write(";end\n")
                fCode.write(";m2")
                fCode.close()
                # --------------------------------------------------------------
                fileName = pathToFolderOutput + deviceName + "x.nc"
                fCode = open(fileName, 'w')
                # --------------------------------------------------------------
                fCode.write(";start control\n")
                fCode.write(f"d0:x{round(dotMin.x)}y{round(dotMin.y)}z0\n")
                fCode.write(";end\n")
                fCode.write(";m2")
                fCode.close()
                # self.PrintCustom("-------------------------------")
                self.print_custom(f"Файл для станка CHM-T36:\n     {fileChmtName}\n")
                self.print_custom(f"Файл для дозатора (калибровочный):\n     {fileNameControl}\n")
                self.print_custom(f"Файл для дозатора (основной):\n     {fileName}")
                self.print_custom(f"Файл для дозатора (основной):\n     {fileName}")
                self.print_custom("-------------------------------")

                # --------------------------------------------------------------
                fileNameInput = pathToFolderOutput + deviceName + "input" + str(razmerX) + "x" + str(razmerY) + ".txt"
                file_input = pathToFolder + "input.txt"
                shutil.copy(file_input, fileNameInput)
                # --------------------------------------------------------------
                if (copyToSdDosator):
                    if (len(drivesRem) == 1):
                        shutil.copy(fileNameControl, fileSd)
                        shutil.copy(fileNameMain, fileSd)
                        shutil.copy(fileName, fileSd)
                        shutil.copy(fileName, fileSd)
                    if (len(drivesRem) == 0):
                        ctypes.windll.user32.MessageBoxW(0, u"Не найдена SD-карта!\nФайл не записан.", u"Ошибка", 0)
                    if (len(drivesRem) > 1):
                        ctypes.windll.user32.MessageBoxW(0,
                                                         u"Найдено больше одной SD-карты, оставьте нужную!\nФайл не записан.",
                                                         u"Ошибка", 0)

                random.seed()

                if showPlot:
                    axesX = []
                    axesY = []
                    axesXs = []
                    axesYs = []
                    axesXc = []
                    axesYc = []
                    axesXr = [0, 0]
                    axesYr = [0, 0]
                    axesXl = []
                    axesYl = []
                    axesTxl = []
                    axesTyl = []
                    plt.ion()
                    for i in coordsSort:
                        if (axesXr[1] < i.x / 100):
                            axesXr[1] = i.x / 100 + 5
                        if (axesYr[1] < i.y / 100):
                            axesYr[1] = i.y / 100 + 5
                    if (True):
                        for k in components:
                            if (k.value != ""):
                                plt.text(k.center.x - len(k.value) / 2, k.center.y + 0.5 + random.random(), k.value)
                            else:
                                plt.text(k.center.x - len(k.type) / 2, k.center.y + 0.5, k.type)
                            axesXc.append(k.center.x)
                            axesYc.append(k.center.y)
                            # for k in coordsSort:
                    #    axesXc.append(k.x) 
                    #    axesYc.append(k.y)
                    lineFlag = False
                    for i in coordsCal:
                        axesTxl.append(i.x / 100)
                        axesTyl.append(i.y / 100)
                    for i in coordsSave:
                        axesXs.append(i.x)
                        axesYs.append(i.y)
                    for i in coordsSort:
                        axesX.append(i.x / 100)
                        axesY.append(i.y / 100)
                        if (True):
                            if (i.line == 1):
                                lineFlag = True
                                axesXl.append(i.x / 100)
                                axesYl.append(i.y / 100)
                            else:
                                if (lineFlag == True):
                                    lineFlag = False
                                    axesXl.append(i.x / 100)
                                    axesYl.append(i.y / 100)
                    plt.plot(axesX, axesY, 'ro')
                    plt.plot(axesXc, axesYc, 'g+')
                    plt.plot(axesTxl, axesTyl, 'bs')
                    plt.axis('equal')
                    plt.draw()
                    # plt.pause(0.1)
                    plt.ioff()
                    plt.show()

            fOptionsLines = []
            fOptionsLines.append(NUMBER_NAME + ") " + str(deviceName))
            fOptionsLines.append(NUMBER_RAZMER_X + ") " + str(razmerX))
            fOptionsLines.append(NUMBER_RAZMER_Y + ") " + str(razmerY))
            fOptionsLines.append(NUMBER_KOLVO_X + ") " + str(kolvoX))
            fOptionsLines.append(NUMBER_KOLVO_Y + ") " + str(kolvoY))
            fOptionsLines.append(NUMBER_SHOW_PLOT + ") " + str(showPlot))
            fOptionsLines.append(NUMBER_SD_CHMT + ") " + str(copyToSdChmt))
            fOptionsLines.append(NUMBER_SD_DOSATOR + ") " + str(copyToSdDosator))
            fOptionsLines.append(NUMBER_SPLIT_SIZE + ") " + str(splitSizeType))
            for kat in range(KOLVO_KATUSHEK):
                fOptionsLines.append("k" + str(kat + 1) + ") " + katushki[kat])

            fOptions = open(pathToFolder + "optionsSP.txt", 'w')
            for strInput in fOptionsLines:
                fOptions.write(strInput + "\n")
                # self.PrintCustom(strInput)
            fOptions.close()
            # ***********************************************************************


class displayApp(App):

    # Создание всех виджетов (объектов)
    def __init__(self):
        super().__init__()

    def kek(self):
        print('ok')

    def on_start(self):
        global deviceName
        global razmerX
        global razmerY
        global splitSizeType
        global kolvoX
        global kolvoY
        global showPlot
        global copyToSdChmt
        global copyToSdDosator
        global pathToFolder
        global pathToFolderOutput
        global katushki

        blKatL = BoxLayout()
        blKatL.orientation = "vertical"
        blKatR = BoxLayout()
        blKatR.orientation = "vertical"
        for kat in range(KOLVO_KATUSHEK):
            num = KOLVO_KATUSHEK - kat - 1
            blKat = BoxLayout()
            blKat.orientation = "horizontal"
            textStr = "№" + str(num + 1)
            if (kat < KOLVO_LOTKOV):
                textStr = textStr + "(" + str(3 - kat) + ")"
            katLabel = Label(text=textStr)
            katTextInput = TextInput(hint_text="1")
            katTextInput.id = "kat" + str(num + 1)
            self.root.ids[katTextInput.id] = katTextInput
            katTextInput.size_hint = (2, 1)
            katTextInput.background_color = (1, 1, 0, 1)
            cbEnable = CheckBox(active=True)
            cbEnable.id = "enKat" + str(num + 1)
            cbEnable.color = (1, 0, 1, 1)
            blKat.add_widget(katLabel)
            # blKat.add_widget(cbEnable)
            blKat.add_widget(katTextInput)
            if (num % 2):
                blKatR.add_widget(blKat)
            else:
                blKatL.add_widget(blKat)
        katTextInputq = TextInput(hint_text="1")
        katTextInputq.id = "kat"
        self.root.blKatushki.orientation = "horizontal"
        self.root.blKatushki.add_widget(blKatL)
        self.root.blKatushki.add_widget(blKatR)

        lastSlash = pathToFolder.rfind("\\")
        pathToFolder = pathToFolder[:lastSlash + 1]
        pathToFolderOutput = pathToFolder[:-1]
        lastSlash = pathToFolderOutput.rfind("\\")
        pathToFolderOutput = pathToFolder[:lastSlash + 1]
        # Read
        pathToFile = pathToFolder + "optionsSP.txt"
        fOptions = open(pathToFile, 'r')
        # Шаблон: х) параметр
        prevI = 0
        fOptionsLines = fOptions.readlines()
        for strInput in fOptionsLines:
            if (strInput[0] == NUMBER_NAME):
                deviceName = strInput[3:-1]
            if (strInput[0] == NUMBER_RAZMER_X):
                razmerX = float(strInput[3:-1])
            if (strInput[0] == NUMBER_RAZMER_Y):
                razmerY = float(strInput[3:-1])
            if (strInput[0] == NUMBER_KOLVO_X):
                kolvoX = int(strInput[3:-1])
            if (strInput[0] == NUMBER_KOLVO_Y):
                kolvoY = int(strInput[3:-1])
            if (strInput[0] == NUMBER_SPLIT_SIZE):
                if (strInput.find("False") != -1):
                    splitSizeType = False
                else:
                    splitSizeType = True
            if (strInput[0] == NUMBER_SHOW_PLOT):
                if (strInput.find("False") != -1):
                    showPlot = False
                else:
                    showPlot = True
            if (strInput[0] == NUMBER_SD_CHMT):
                if (strInput.find("False") != -1):
                    copyToSdChmt = False
                else:
                    copyToSdChmt = True
            if (strInput[0] == NUMBER_SD_DOSATOR):
                if (strInput.find("False") != -1):
                    copyToSdDosator = False
                else:
                    copyToSdDosator = True
            if (strInput[0] == "k"):
                pos = strInput.find(")")
                i = int(strInput[1:pos]) - 1
                if (i > prevI + 1):
                    j = prevI + 1
                    while (j < i):
                        smdKat = Smd(j, " ", " ")
                        stacks.append(smdKat)
                        j += 1
                prevI = i
                katushki[i] = strInput[pos + 2:-1]
                paramKat = katushki[i].split()
                if (len(paramKat) < 2):
                    paramKat = [" ", " "]
                smdKat = Smd(i + 1, paramKat[0], paramKat[1])
                stacks.append(smdKat)
                self.root.ids[str("kat" + str(i + 1))].text = katushki[i]
        fOptions.close()

        self.root.tiName.text = deviceName
        self.root.tiRazmerX.text = str(razmerX)
        self.root.tiRazmerY.text = str(razmerY)
        self.root.tiKolvoX.text = str(kolvoX)
        self.root.tiKolvoY.text = str(kolvoY)
        self.root.cbGrafik.active = showPlot
        self.root.cbSdChmt.active = copyToSdChmt
        self.root.cbSdDosator.active = copyToSdDosator
        self.root.cbSplitSize.active = splitSizeType

        # print(self.root.ids)
        # self.root.llOut.text = "sads"

    # Основной метод для построения программы
    def build(self):
        return Container()


# ***********************************************************************
# Запуск проекта
if __name__ == "__main__":
    displayApp().run()
# ***********************************************************************
PressKey('esc')
# ***********************************************************************
