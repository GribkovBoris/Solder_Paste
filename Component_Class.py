# ***********************************************************************
import math
from Point_Class import Point
from Smd_Class import Smd


# ***********************************************************************
class Component:
    DOT_SMALL = 1
    DOT_MEDIUM = 2
    DOT_BIG = 3
    LINE_START = 8
    LINE_END = 9

    class Error:
        def __init__(self):
            self.not_found_in_lib = False

    def __init__(self, center, angle, description, comp_type, pattern_name, value, interface_data_):
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.error = False
        self.pins = None
        self.interface_data = interface_data_
        self.center = center
        self.real_angle = angle
        self.angle = 90 + angle
        self.description = description
        self.type = comp_type
        self.pattern_name = pattern_name
        self.value = value
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.onlyPaste = False
        self.skip = 0
        self.stack = None
        self.sizeType = None
        self.height = None
        self.ignore_rotation = False  # !!!!!!!! TODO
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.error_pattern = self.check_errors()
        self.correct_values()
        self.correct_angles(angle)
        self.init_component_parameters()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def check_errors(self):
        error_flag = False
        if Smd.get_height(self.pattern_name) == "":
            error_flag = True
        return error_flag

    def correct_angles(self, angle):
        if self.pattern_name == "SM-6":
            self.angle = angle
        if self.pattern_name == "SO8":
            self.angle = angle
        if self.pattern_name == "TSSOP_20":
            self.angle = angle
        if self.pattern_name == "SOT-23":
            self.angle = angle
        if self.pattern_name == "ATMEGA8":
            self.angle = angle
        if self.pattern_name == "DB-1S":
            self.angle = self.angle + 180
        if self.angle >= 360:
            self.angle -= 360

    def correct_values(self):
        if self.value == "104":
            self.value = "0.1"
        if (self.pattern_name.find("TLP521") != -1) or (self.value.find("TLP521") != -1) or \
                (self.description.find("TLP521") != -1) or (self.pattern_name.find("K1010") != -1) or \
                (self.value.find("K1010") != -1) or (self.description.find("K1010") != -1):
            self.pattern_name = "K1010"
            self.value = "K1010"
            self.angle = self.angle + 180
        if self.pattern_name == "TO-269AA":
            self.pattern_name = "MB8S"
            self.value = "MB8S"
            self.angle = self.angle + 270
            self.real_angle = self.real_angle + 270
        if self.pattern_name == "0805" and self.value == "3K":
            self.type = "R0805"
        if self.value.find("40-06") != -1:
            self.value = "4006"
        if self.value == "400Kx2":
            self.value = "430K"
        if self.value == "BZV55C":
            self.value = "5V1"
        if self.value == "50K":
            self.value = "51K"
        if self.pattern_name == "DB-1S":
            self.value = "107"
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

    def fill_dots(self):
        if self.pattern_name == "0805":
            self.pins.append(Point(-2.21 / 2, 0, self.DOT_SMALL))
            self.pins.append(Point(2.21 / 2, 0, self.DOT_SMALL))
            if self.angle > 90:
                self.angle -= 180
        if self.pattern_name == "1206":
            self.pins.append(Point(-3.25 / 2, 0, self.DOT_MEDIUM))
            self.pins.append(Point(3.25 / 2, 0, self.DOT_MEDIUM))
            if self.angle > 90:
                self.angle -= 180
        if self.pattern_name == "2512":
            self.pins.append(Point(-3, 0, self.DOT_BIG))
            self.pins.append(Point(3, 0, self.DOT_BIG))
            self.pins.append(Point(-3, 1, self.DOT_BIG))
            self.pins.append(Point(3, 1, self.DOT_BIG))
            self.pins.append(Point(-3, -1, self.DOT_BIG))
            self.pins.append(Point(3, -1, self.DOT_BIG))
            if self.angle > 90:
                self.angle -= 180
        if (self.ignore_rotation and (self.angle <= 90)) or not self.ignore_rotation:
            if (self.pattern_name == "SOD323") or (self.pattern_name == "LED_0805"):
                self.pins.append(Point(-2.21 / 2, 0, self.DOT_SMALL))
                self.pins.append(Point(2.21 / 2, 0, self.DOT_SMALL))
            if self.pattern_name == "10X16":
                self.pins.append(Point(-1.7, 0, self.DOT_MEDIUM))
                self.pins.append(Point(1.7, 0, self.DOT_MEDIUM))
                self.pins.append(Point(-3, 0, self.DOT_MEDIUM))
                self.pins.append(Point(3, 0, self.DOT_MEDIUM))
                if self.value == "22X16":
                    self.pins.append(Point(-4.5, 0, self.DOT_BIG))
                    self.pins.append(Point(4.5, 0, self.DOT_BIG))
                self.angle += 180
                if self.angle >= 360:
                    self.angle -= 360
            if self.pattern_name == "LEDD":
                self.pins.append(Point(-1, 0, self.DOT_SMALL))
                self.pins.append(Point(1, 0, self.DOT_SMALL))
                if self.angle > 90:
                    self.angle -= 180
            if self.pattern_name == "SOT-23":
                self.pins.append(Point(-2.47 / 2, -1.80 / 2, self.DOT_SMALL))
                self.pins.append(Point(2.47 / 2, -1.80 / 2, self.DOT_SMALL))
                self.pins.append(Point(0, 2.47 / 2, self.DOT_SMALL))
            if self.pattern_name == "SOD80_S":
                self.pins.append(Point(-2.2, 0, self.DOT_BIG))
                self.pins.append(Point(-1.20, 0, self.DOT_MEDIUM))
                self.pins.append(Point(1.60, 0, self.DOT_MEDIUM))
                self.pins.append(Point(2.5, 0, self.DOT_BIG))
            if self.pattern_name == "DB-1S":
                self.pins.append(Point(4.20, -2.70, self.DOT_MEDIUM))
                self.pins.append(Point(4.20, 2.70, self.DOT_MEDIUM))
                self.pins.append(Point(-4.20, -2.70, self.DOT_MEDIUM))
                self.pins.append(Point(-4.20, 2.70, self.DOT_MEDIUM))
                self.pins.append(Point(5.40, -2.70, self.DOT_MEDIUM))
                self.pins.append(Point(5.40, 2.70, self.DOT_MEDIUM))
                self.pins.append(Point(-5.40, -2.70, self.DOT_MEDIUM))
                self.pins.append(Point(-5.40, 2.70, self.DOT_MEDIUM))
            if self.pattern_name == "MB8S":
                self.pins.append(Point(3, -1.20, self.DOT_BIG))
                self.pins.append(Point(3, 1.20, self.DOT_BIG))
                self.pins.append(Point(-3, -1.20, self.DOT_BIG))
                self.pins.append(Point(-3, 1.20, self.DOT_BIG))
            if self.pattern_name == "K1010":
                self.pins.append(Point(4, -1.25, self.DOT_MEDIUM))
                self.pins.append(Point(4, 1.25, self.DOT_MEDIUM))
                self.pins.append(Point(4.5, -1.25, self.DOT_MEDIUM))
                self.pins.append(Point(4.5, 1.25, self.DOT_MEDIUM))
                self.pins.append(Point(-4, -1.25, self.DOT_MEDIUM))
                self.pins.append(Point(-4, 1.25, self.DOT_MEDIUM))
                self.pins.append(Point(-4.5, -1.25, self.DOT_MEDIUM))
                self.pins.append(Point(-4.5, 1.25, self.DOT_MEDIUM))
            if self.pattern_name == "DIP4":
                self.pins.append(Point(4.20, -1.2, self.DOT_MEDIUM))
                self.pins.append(Point(4.20, 1.2, self.DOT_MEDIUM))
                self.pins.append(Point(-4.20, -1.2, self.DOT_MEDIUM))
                self.pins.append(Point(-4.20, 1.2, self.DOT_MEDIUM))
            if self.pattern_name == "SM-6":
                self.pins.append(Point(4.62, -2.36, self.DOT_BIG))
                self.pins.append(Point(4.62, 2.36, self.DOT_BIG))
                self.pins.append(Point(-4.64, -0.17, self.DOT_BIG))
                self.pins.append(Point(-4.64, 2.36, self.DOT_BIG))
            if self.pattern_name == "SO8":
                self.pins.append(Point(-3.1, 1.90, self.DOT_SMALL))
                self.pins.append(Point(-3.1, 0.63, self.DOT_SMALL))
                self.pins.append(Point(-3.1, -0.63, self.DOT_SMALL))
                self.pins.append(Point(-3.1, -1.90, self.DOT_SMALL))
                self.pins.append(Point(3.1, 1.90, self.DOT_SMALL))
                self.pins.append(Point(3.1, 0.63, self.DOT_SMALL))
                self.pins.append(Point(3.1, -0.63, self.DOT_SMALL))
                self.pins.append(Point(3.1, -1.90, self.DOT_SMALL))
            if self.pattern_name == "TSSOP_20":
                self.pins.append(Point(-2.8, 3.10, self.DOT_SMALL))
                self.pins.append(Point(-2.8, -3.10, self.DOT_SMALL))
                self.pins.append(Point(2.8, 3.10, self.DOT_SMALL))
                self.pins.append(Point(2.8, -3.10, self.DOT_SMALL))
            if self.pattern_name == "SOT-223":
                self.pins.append(Point(-2.3, -3, self.DOT_MEDIUM))
                self.pins.append(Point(0, -3, self.DOT_MEDIUM))
                self.pins.append(Point(2.3, -3, self.DOT_MEDIUM))
                self.pins.append(Point(0, 3, self.DOT_MEDIUM))
            if self.pattern_name == "64A":  # lNog=12.4, half=6.2; lCorp=15.4, half=7.7
                self.pins.append(Point(-5.2, -7.7, self.DOT_MEDIUM))
                self.pins.append(Point(-3.2, -7.7, self.DOT_MEDIUM))
                self.pins.append(Point(-1.2, -7.7, self.DOT_MEDIUM))
                self.pins.append(Point(1.2, -7.7, self.DOT_MEDIUM))
                self.pins.append(Point(3.2, -7.7, self.DOT_MEDIUM))
                self.pins.append(Point(5.2, -7.7, self.DOT_MEDIUM))
                self.pins.append(Point(-5.2, 7.7, self.DOT_MEDIUM))
                self.pins.append(Point(-3.2, 7.7, self.DOT_MEDIUM))
                self.pins.append(Point(-1.2, 7.7, self.DOT_MEDIUM))
                self.pins.append(Point(1.2, 7.7, self.DOT_MEDIUM))
                self.pins.append(Point(3.2, 7.7, self.DOT_MEDIUM))
                self.pins.append(Point(5.2, 7.7, self.DOT_MEDIUM))
                self.pins.append(Point(-7.7, -5.2, self.DOT_MEDIUM))
                self.pins.append(Point(-7.7, -3.2, self.DOT_MEDIUM))
                self.pins.append(Point(-7.7, -1.2, self.DOT_MEDIUM))
                self.pins.append(Point(-7.7, 1.2, self.DOT_MEDIUM))
                self.pins.append(Point(-7.7, 3.2, self.DOT_MEDIUM))
                self.pins.append(Point(-7.7, 5.2, self.DOT_MEDIUM))
                self.pins.append(Point(7.7, -5.2, self.DOT_MEDIUM))
                self.pins.append(Point(7.7, -3.2, self.DOT_MEDIUM))
                self.pins.append(Point(7.7, -1.2, self.DOT_MEDIUM))
                self.pins.append(Point(7.7, 1.2, self.DOT_MEDIUM))
                self.pins.append(Point(7.7, 3.2, self.DOT_MEDIUM))
                self.pins.append(Point(7.7, 5.2, self.DOT_MEDIUM))
            if self.pattern_name == "ATMEGA8":  # lNog=6.2, half=3.1; lCorp=9.2, half=4.6
                self.pins.append(Point(-3.05, 4.6, self.DOT_SMALL))
                self.pins.append(Point(-1.05, 4.6, self.DOT_SMALL))
                self.pins.append(Point(1.05, 4.6, self.DOT_SMALL))
                self.pins.append(Point(3.05, 4.6, self.DOT_SMALL))
                self.pins.append(Point(-3.05, -4.6, self.DOT_SMALL))
                self.pins.append(Point(-1.05, -4.6, self.DOT_SMALL))
                self.pins.append(Point(1.05, -4.6, self.DOT_SMALL))
                self.pins.append(Point(3.05, -4.6, self.DOT_SMALL))
                self.pins.append(Point(4.6, -3.05, self.DOT_SMALL))
                self.pins.append(Point(4.6, -1.05, self.DOT_SMALL))
                self.pins.append(Point(4.6, 1.05, self.DOT_SMALL))
                self.pins.append(Point(4.6, 3.05, self.DOT_SMALL))
                self.pins.append(Point(-4.6, -3.05, self.DOT_SMALL))
                self.pins.append(Point(-4.6, -1.05, self.DOT_SMALL))
                self.pins.append(Point(-4.6, 1.05, self.DOT_SMALL))
                self.pins.append(Point(-4.6, 3.05, self.DOT_SMALL))

    def init_component_parameters(self):
        self.stack = 0
        self.height = 0.5
        self.error = True
        self.sizeType = Smd.get_size_type(self.pattern_name)
        for st in self.interface_data.stacks:
            st_value = st.value
            self.skip = 0
            if self.pattern_name == st.pattern_name and st.number != 0 and self.value == st_value:
                self.stack = st.number
                self.height = st.height
                self.error = False
                break

        if not self.error:
            self.pins = []
            self.fill_dots()

            if self.angle < 0:
                self.angle += 360
            if len(self.pins) == 0:
                self.error = True
            else:
                for pin in self.pins:
                    xz = self.center.x + pin.x * math.cos(self.real_angle * math.pi / 180) - \
                         pin.y * math.sin(self.real_angle * math.pi / 180)
                    yz = self.center.y + pin.x * math.sin(self.real_angle * math.pi / 180) + \
                         pin.y * math.cos(self.real_angle * math.pi / 180)
                    pin.x = xz
                    pin.y = yz

# ***********************************************************************