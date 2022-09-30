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

    def __init__(self, number, pattern_name, value):
        self.number = number
        self.value = value
        self.pattern_name = pattern_name
        self.height = 0
        self.height = self.get_height(pattern_name)

    @staticmethod
    def get_param(pattern_name, param_number):
        param = 0
        try:
            param = Smd.smdParams[pattern_name][param_number]
        except LookupError:
            print("Компонент не найден в библиотеке")
        return param


    @staticmethod
    def get_height(pattern_name):
        return Smd.get_param(pattern_name, 0)

    @staticmethod
    def get_x_offset(pattern_name):
        return Smd.get_param(pattern_name, 1)

    @staticmethod
    def get_y_offset(pattern_name):
        return Smd.get_param(pattern_name, 2)

    @staticmethod
    def get_feed_rate(pattern_name):
        return Smd.get_param(pattern_name, 3)

    @staticmethod
    def get_size_type(pattern_name):
        return Smd.get_param(pattern_name, 4)
