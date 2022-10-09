# ==================================================================
import os
import shutil
import matplotlib.pyplot as plt
import random
import win32api
import win32file
import ctypes
import tkinter as tk
from tkinter import filedialog
import math

from Component_Class import Component
# ==================================================================
from Gui_Automizer import GuiAutomizer
from Gui_Automizer import MyThread
from Smd_Class import Smd
from Interface_Data_Class import InterfaceData
from Point_Class import Point


# ==================================================================
def get_path_to_folder():
    path_to_file = os.path.abspath(__file__)
    last_slash = path_to_file.rfind("\\")
    path_to_folder = path_to_file[:last_slash + 1]
    return path_to_folder


# ***********************************************************************
class PcadConverter:
    # ***********************************************************************
    NUMBER_NAME = "1"
    NUMBER_SIZE_X = "2"
    NUMBER_SIZE_Y = "3"
    NUMBER_NUMBER_X = "4"
    NUMBER_NUMBER_Y = "5"
    NUMBER_SHOW_PLOT = "6"
    NUMBER_SD_CHMT = "7"
    NUMBER_SD_DISPENSER = "8"
    NUMBER_SPLIT_SIZE = "9"
    # ***********************************************************************
    DRIVE_REMOVABLE = 2
    # ***********************************************************************
    FIRST_STRING = b'%,\xd4\xad\xb5\xe3\xc6\xab\xd2\xc6,X,Y,'
    SECOND_STRING = b'%,\xc1\xcf\xd5\xbb\xc6\xab\xd2\xc6,\xc1\xcf\xd5\xbb\xba\xc5,X,Y,\xbd\xf8\xb8\xf8\xc1\xbf,' \
                    b'\xd7\xa2\xca\xcd '
    THIRD_STRING = b'%,\xc6\xb4\xb0\xe51,X,Y,'
    FOURTH_STRING = b'%,\xcc\xf9\xcd\xb7\xba\xc5,\xc1\xcf\xd5\xbb\xba\xc5,X,Y,\xbd\xc7\xb6\xc8,\xb8\xdf\xb6\xc8,' \
                    b'\xcc\xf8\xb9\xfd,\xcb\xd9\xb6\xc8,\xcb\xb5\xc3\xf7,\xd7\xa2\xca\xcd '

    # ***********************************************************************

    def __init__(self):
        self.coords_sort = None
        self.components_fail = None
        self.path_to_folder = get_path_to_folder()
        self.path_to_folder_output = self.path_to_folder
        self.file_chmt_name = ""
        self.file_dispenser_name_control = ""
        self.file_dispenser_name_main = ""
        self.file_dispenser_name_size = ""
        self.components = []
        self.out_text = ""
        self.interface_data = None
        self.drives_rem = []
        self.stack_error = 0
        # ***********************************************************************
        self.file_sd = "E:/"
        self.allow_convert = 0
        self.ignore_coef = 0
        self.coord_coef = 0.801
        self.x_coef = 1.0
        self.y_coef = 1.0
        self.size_type_small = True
        self.chmtx_coef = 1.0
        self.chmty_coef = 1.0
        self.path_to_file = ""
        self.coords_cal = None

    @staticmethod
    def input_pcad():
        path_to_folder = get_path_to_folder()
        file_input = path_to_folder + "Input.txt"
        file_out = open(file_input, 'w')
        input_text = GuiAutomizer.pcad_reports()
        # input_text = pyperclip.paste()
        input_text = input_text.replace('\n', '')
        print(input_text)
        file_out.write(input_text)
        file_out.close()

    @staticmethod
    def call_file_picker():
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename(filetypes=[("Correct file", ".csv")])

    @staticmethod
    def find_file_with_same_name(directory, file_name):
        """
        Find file in directory, that has same name with received
        :param directory: in which directory search file
        :param file_name: name of file that need to be found
        :return: bool, file found
        """
        files = os.listdir(directory)
        main_file_path = ""
        for f in files:
            if file_name.find(f) != -1:
                main_file_path = directory + "\\" + f
                break
        return main_file_path != ""

    def run_graph_builder(self):
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
        for i in self.coords_sort:
            if axes_xr[1] < i.x / 100:
                axes_xr[1] = i.x / 100 + 5
            if axes_yr[1] < i.y / 100:
                axes_yr[1] = i.y / 100 + 5
        for k in self.components:
            if k.value != "":
                plt.text(k.center.x - len(k.value) / 2, k.center.y + 0.5 + random.random(), k.value)
            else:
                plt.text(k.center.x - len(k.type) / 2, k.center.y + 0.5, k.type)
            axes_xc.append(k.center.x)
            axes_yc.append(k.center.y)
        line_flag = False
        for i in self.coords_cal:
            axes_t_xl.append(i.x / 100)
            axes_t_yl.append(i.y / 100)
        for i in self.coords_save:
            axes_xs.append(i.x)
            axes_ys.append(i.y)
        for i in self.coords_sort:
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

    def set_interface_data(self, interface_data_: InterfaceData):
        self.interface_data = interface_data_
    def get_interface_data(self):
        return self.interface_data

    def correct_coords(self):
        point = self.path_to_folder.rfind("\\")
        this_directory = self.path_to_folder[:point]
        point = this_directory.rfind("\\")
        this_directory = self.path_to_folder[:point]

        file_path = self.call_file_picker()  # call window that allows to pick file
        point = file_path.rfind("/") + 1
        input_file_name = file_path[point:]
        input_file = file_path

        main_file_path = self.find_file_with_same_name(directory=this_directory, file_name=input_file_name)
        if main_file_path == "":
            print("Нет файла импорта")
            input_file = ""
        error = False

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
                input_text = GuiAutomizer.pcad_correct_coords(arr_coords)

                file_input = self.path_to_folder + "Input.txt"
                file_out = open(file_input, 'w')
                input_text = input_text.replace('\n', '')
                # print(input_text)
                file_out.write(input_text)
                file_out.close()

    def create_dispenser_files(self):
        # ----- Подготовка файла для дозатора -----
        # ------------ Read PNP file --------------
        # --------------------------------------------------------------
        # Coord ged and mux coeff
        coords = []
        self.coords_save = []
        for com in self.components:
            for coord in com.pins:
                coords.append(coord)
        for com in coords:
            self.coords_save.append(com)
        # --------------------------------------------------------------
        self.print_custom(f"Количество точек - {len(coords)}")
        # --------------------------------------------------------------
        self.coords_sort = []

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
        self.coords_sort.append(dot)
        coords.pop(index_min)
        # --------------------------------------------------------------
        cnt = 0
        while len(coords) > 0:
            lenq = 0.0
            min_len = 0.0
            min_len_index = 0
            for i in range(len(coords)):
                # if(coords[i].line != LINE_END):
                lenq = math.sqrt(math.pow((coords[i].x - self.coords_sort[-1].x), 2) +
                                 math.pow((coords[i].y - self.coords_sort[-1].y), 2))
                if (min_len == 0) or (min_len > lenq):
                    min_len = lenq
                    min_len_index = i

            qdot = Point(coords[min_len_index].x, coords[min_len_index].y, coords[min_len_index].line)
            self.coords_sort.append(qdot)
            coords.pop(min_len_index)
            if qdot.line == Component.LINE_START:
                qdot = Point(coords[min_len_index].x, coords[min_len_index].y, coords[min_len_index].line)
                self.coords_sort.append(qdot)
                coords.pop(min_len_index)
            else:
                if qdot.line == Component.LINE_END:
                    qdot = Point(coords[min_len_index - 1].x, coords[min_len_index - 1].y,
                                 coords[min_len_index - 1].line)
                    self.coords_sort.append(qdot)
                    coords.pop(min_len_index - 1)
        # --------------------------------------------------------------
        coords_num = len(self.coords_sort)
        for board_x in range(self.interface_data.devices_number_x):
            for board_y in range(self.interface_data.devices_number_y):
                if (board_x > 0) or (board_y > 0):
                    for coord in range(coords_num):
                        qdot = Point(self.coords_sort[coord].x + self.interface_data.size_x * board_x,
                                     self.coords_sort[coord].y + self.interface_data.size_y * board_y,
                                     self.coords_sort[coord].line)
                        self.coords_sort.append(qdot)
        # --------------------------------------------------------------
        if True:
            dot_max = Point(0, 0)
            len_max = 0.0
            for i in range(0, len(self.coords_sort) - 1):
                lenq = math.sqrt(math.pow(self.coords_sort[i].x, 2) + math.pow(self.coords_sort[i].y, 2))
                if (len_max == 0.0) or (len_max < lenq):
                    len_max = lenq
                    dot_max.x = self.coords_sort[i].x
                    dot_max.y = self.coords_sort[i].y

        dot_max_b = Point(dot_max.x,
                          dot_max.y - (self.interface_data.devices_number_y - 1) * self.interface_data.size_y)
        dot_max_t = Point(dot_min.x,
                          dot_min.y + (self.interface_data.devices_number_y - 1) * self.interface_data.size_y)

        self.coords_cal = [dot_min, dot_max, dot_max_t, dot_max_b]

        dot_min.x = dot_min.x * 100
        dot_min.y = dot_min.y * 100
        dot_max.x = dot_max.x * 100
        dot_max.y = dot_max.y * 100
        dot_max_t.x = dot_max_t.x * 100
        dot_max_t.y = dot_max_t.y * 100
        dot_max_b.x = dot_max_b.x * 100
        dot_max_b.y = dot_max_b.y * 100

        # --------------------------------------------------------------
        # --------- Dispenser file output ------------------------------
        # --------------------------------------------------------------
        self.file_dispenser_name_main = self.path_to_folder_output + self.interface_data.device_name + ".nc"
        file_dispenser_main = open(self.file_dispenser_name_main, 'w')
        # --------------------------------------------------------------
        file_dispenser_main.write(";start main\n")
        # --------------------------------------------------------------
        for i in range(len(self.coords_sort)):
            self.coords_sort[i].x = (self.coords_sort[i].x * 100)
            self.coords_sort[i].y = (self.coords_sort[i].y * 100)
            if (self.coords_sort[i].line == Component.LINE_START) or \
                    (self.coords_sort[i].line == Component.LINE_END):
                prefix = "l"
            else:
                prefix = "d" + str(self.coords_sort[i].line)
            file_dispenser_main.write(f"{prefix}:x{round(self.coords_sort[i].x)}y{round(self.coords_sort[i].y)}z0\n")
        # --------------------------------------------------------------
        file_dispenser_main.write(f"d0:x0y0z0\n")
        file_dispenser_main.write(";end\n")
        file_dispenser_main.write(";m2")
        file_dispenser_main.close()
        # --------------------------------------------------------------
        self.file_dispenser_name_size = self.path_to_folder_output + self.interface_data.device_name + "T.nc"
        file_dispenser_size = open(self.file_dispenser_name_size, 'w')
        file_dispenser_size.write(";start size\n")
        file_dispenser_size.write(f"d0:x{round(dot_min.x)}y{round(dot_min.y)}z0\n")
        file_dispenser_size.write(f"d0:x{round(dot_max_t.x)}y{round(dot_max_t.y)}z0\n")
        file_dispenser_size.write(f"d0:x{round(dot_max.x)}y{round(dot_max.y)}z0\n")
        file_dispenser_size.write(f"d0:x{round(dot_max_b.x)}y{round(dot_max_b.y)}z0\n")
        file_dispenser_size.write(f"d0:x0y0z0\n")
        file_dispenser_size.write(";end\n")
        file_dispenser_size.write(";m2")
        file_dispenser_size.close()
        # --------------------------------------------------------------
        self.file_dispenser_name_control = self.path_to_folder_output + self.interface_data.device_name + "X.nc"
        file_dispenser_control = open(self.file_dispenser_name_control, 'w')
        # --------------------------------------------------------------
        file_dispenser_control.write(";start control\n")
        file_dispenser_control.write(f"d0:x{round(dot_min.x)}y{round(dot_min.y)}z0\n")
        file_dispenser_control.write(";end\n")
        file_dispenser_control.write(";m2")
        file_dispenser_control.close()
        # self.PrintCustom("-------------------------------")

        # --------------------------------------------------------------
        file_input_name = self.path_to_folder_output + self.interface_data.device_name + \
                          "input" + str(self.interface_data.size_x) + "x" + str(self.interface_data.size_y) + ".txt"
        file_input = self.path_to_folder + "input.txt"
        shutil.copy(file_input, file_input_name)
        # --------------------------------------------------------------
        if self.interface_data.copy_to_sd_dispenser:
            file_sd = self.get_drive()
            if file_sd is not None:
                if len(self.drives_rem) == 1:
                    shutil.copy(self.file_dispenser_name_control, file_sd)
                    shutil.copy(self.file_dispenser_name_main, file_sd)
                    shutil.copy(self.file_dispenser_name_size, file_sd)
                if len(self.drives_rem) == 0:
                    ctypes.windll.user32.MessageBoxW(0, u"Не найдена SD-карта!\nФайл не записан.", u"Ошибка", 0)
                if len(self.drives_rem) > 1:
                    ctypes.windll.user32.MessageBoxW(0, u"Найдено больше одной SD-карты, оставьте нужную!\nФайл "
                                                        u"не записан.", u"Ошибка", 0)

    def create_chmt_files(self):
        split_count = 1
        number_components = 0
        number_auto = 0
        number_decline = 0
        if self.interface_data.split_size_type:
            split_count = 2
        for split_file in range(split_count):
            fin = open(self.path_to_file, 'r')
            if split_file:
                size_type_small = True
            else:
                size_type_small = False
            # Write
            if self.interface_data.split_size_type:
                if size_type_small:
                    mark_file = "s"
                else:
                    mark_file = "b"
            else:
                mark_file = ""
            self.file_chmt_name = self.path_to_folder_output + self.interface_data.device_name + mark_file + ".csv"
            file_out = open(self.file_chmt_name, 'w')
            # ---------------------- Origin offset ----------------------
            file_out.close()
            file_out = open(self.file_chmt_name, 'ab')
            # FIRST_STRING = b'\x25\x2c\xd4\xad\xb5\xe3\xc6\xab\xd2\xc6'
            file_out.write(self.FIRST_STRING)
            file_out.close()
            file_out = open(self.file_chmt_name, 'a')
            file_out.write("\n")
            file_out.write("65535,0,")
            file_out.write("0")
            file_out.write(",")
            file_out.write("0")
            file_out.write(",")
            file_out.write("0")
            file_out.write(",")
            file_out.write("0")
            file_out.write("\n\n")
            # ---------------------- List of stacks ----------------------
            # c1cfd5bbc6abd2c6
            file_out.close()
            file_out = open(self.file_chmt_name, 'ab')
            # SECOND_STRING = b'\x25\x2c\xc1\xcf\xd5\xbb\xc6\xab\xd2\xc6'
            file_out.write(self.SECOND_STRING)
            file_out.close()
            file_out = open(self.file_chmt_name, 'a')
            file_out.write("\n")
            feed_rate = 2
            for kat in self.interface_data.stacks:
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
            file_out = open(self.file_chmt_name, 'ab')
            # THIRD_STRING = b'\x25\x2c\xc6\xb4\xb0\xe5\x31\x2c\x58'
            file_out.write(self.THIRD_STRING)
            file_out.close()
            file_out = open(self.file_chmt_name, 'a')
            file_out.write("\n")
            file_out.write("65535,")
            if self.interface_data.size_x * self.interface_data.size_y == 1:
                file_out.write(str(3))
            else:
                file_out.write(str(4))
            file_out.write(",")
            file_out.write(f"{self.interface_data.size_x},{self.interface_data.size_y},")
            file_out.write(f"{self.interface_data.devices_number_x},{self.interface_data.devices_number_y}\n\n")
            # ---------------------- List of self.components ----------------------
            # ccf9cdb7bac5
            file_out.close()
            file_out = open(self.file_chmt_name, 'ab')
            # FOURTH_STRING = b'\x25\x2c\xcc\xf9\xcd\xb7\xba\xc5'
            file_out.write(self.FOURTH_STRING)
            file_out.close()
            file_out = open(self.file_chmt_name, 'a')
            file_out.write("\n")
            # ----------------------------------------------------------------
            speed = 100
            head = 1

            self.components_fail = []
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
                    # RefDes,Name,Type,Value,Layer,X,Y,Rotation
                    description = properties[0]
                    prop_name = properties[1]
                    comment = properties[2]
                    value = properties[3]
                    prop_layer = properties[4]
                    x = float(properties[5])
                    y = float(properties[6])
                    angle = float(properties[7])

                    cur_comp = Component(Point(x, y), angle, description, comment, prop_name, value,
                                         self.interface_data)

                    found = False
                    number_components += 1
                    if not cur_comp.error:
                        self.components.append(cur_comp)
                        found = True
                        # Формирование кода для станка
                        number_auto += 1
                        # if(not self.root.ids[str("cbKat"+str(kat.number))].enabled):
                        #   flag = False
                        if not self.interface_data.split_size_type:
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
                        self.components_fail.append(cur_comp)
            file_out.close()
            fin.close()
            # print(len(self.drives_rem))
            if self.interface_data.copy_to_sd_chmt:
                file_sd = self.get_drive()
                if file_sd is not None:
                    if not self.interface_data.split_size_type:
                        file_chmt_name = self.interface_data.path_to_folder_output + \
                                         self.interface_data.device_name + ".csv"
                        shutil.copy(file_chmt_name, file_sd)
                    else:
                        file_chmt_name = self.interface_data.path_to_folder_output + \
                                         self.interface_data.device_name + "s" + ".csv"
                        shutil.copy(file_chmt_name, file_sd)
                        file_chmt_name = self.interface_data.path_to_folder_output + \
                                         self.interface_data.device_name + "b" + ".csv"
                        shutil.copy(file_chmt_name, file_sd)

        self.print_custom(f"Количество компонентов - {number_components}")
        self.print_custom(f"Количество компонентов автоматической пайки - {number_auto}")
        self.print_custom(f"Количество необработанных компонентов - {number_decline}:")

        i = 0
        type_unique = []
        value_unique = []
        for k in self.components_fail:
            if len(type_unique) == 0:
                allow_adding = True
            else:
                allow_adding = True
                for kk in range(len(type_unique)):
                    if (k.type == type_unique[kk]) and (k.value == value_unique[kk]):
                        allow_adding = False
            if allow_adding:
                type_unique.append(k.type)
                value_unique.append(k.value)
                i += 1
                self.print_custom(f"{i}) {k.description}, {k.pattern_name}, {k.value}")
        # --------------------------------------------------------------

    def get_drive(self):
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        drives_rem = []
        for root in drives:
            if win32file.GetDriveTypeW(root) == self.DRIVE_REMOVABLE:
                self.drives_rem.append(root)
        file_sd = None
        if len(drives_rem) == 1:
            file_sd = drives_rem[0]
        if len(drives_rem) == 0:
            ctypes.windll.user32.MessageBoxW(0, u"Не найдена SD-карта!\nФайл не записан.", u"Ошибка", 0)
        if len(drives_rem) > 1:
            ctypes.windll.user32.MessageBoxW(0, u"Найдено больше одной SD-карты, оставьте нужную!\nФайл не "
                                                u"записан.", u"Ошибка", 0)
        return file_sd

    def read_options_file(self):
        path_to_folder = get_path_to_folder()
        # Read1
        path_to_file = path_to_folder + "optionsSP.txt"
        file_options = open(path_to_file, 'r')
        # Шаблон: х) параметр
        prev_i = 0
        file_options_lines = file_options.readlines()
        for str_input in file_options_lines:
            if str_input[0] == self.NUMBER_NAME:
                self.interface_data.device_name = str_input[3:-1]
            if str_input[0] == self.NUMBER_SIZE_X:
                self.interface_data.size_x = float(str_input[3:-1])
            if str_input[0] == self.NUMBER_SIZE_Y:
                self.interface_data.size_y = float(str_input[3:-1])
            if str_input[0] == self.NUMBER_NUMBER_X:
                self.interface_data.devices_number_x = int(str_input[3:-1])
            if str_input[0] == self.NUMBER_NUMBER_Y:
                self.interface_data.devices_number_y = int(str_input[3:-1])
            if str_input[0] == self.NUMBER_SPLIT_SIZE:
                if str_input.find("False") != -1:
                    self.interface_data.split_size_type = False
                else:
                    self.interface_data.split_size_type = True
            if str_input[0] == self.NUMBER_SHOW_PLOT:
                if str_input.find("False") != -1:
                    self.interface_data.show_plot = False
                else:
                    self.interface_data.show_plot = True
            if str_input[0] == self.NUMBER_SD_CHMT:
                if str_input.find("False") != -1:
                    self.interface_data.copy_to_sd_chmt = False
                else:
                    self.interface_data.copy_to_sd_chmt = True
            if str_input[0] == self.NUMBER_SD_DISPENSER:
                if str_input.find("False") != -1:
                    self.interface_data.copy_to_sd_dispenser = False
                else:
                    self.interface_data.copy_to_sd_dispenser = True
            if str_input[0] == "k":
                pos = str_input.find(")")
                i = int(str_input[1:pos]) - 1
                print(i)
                if i > prev_i + 1:
                    j = prev_i + 1
                    while j < i:
                        self.interface_data.stacks.append(Smd(j, "", ""))
                        j += 1
                prev_i = i
                param_kat = str_input[pos + 2:-1].split()
                if len(param_kat) < 2:
                    param_kat = [" ", " ", 0]
                if len(param_kat) == 2:
                    param_kat.append(0)
                if i >= self.interface_data.NUMBER_COILS + self.interface_data.NUMBER_TRAYS:
                    param_kat[2] = 1
                    print('dos')
                    param_kat[0] = str(i) + ':' + str(param_kat[2])
                if param_kat[0] == " ":
                    param_kat[0] = ''
                if param_kat[1] == " ":
                    param_kat[1] = ''
                smd_kat = Smd(i + 1, param_kat[0], param_kat[1], int(param_kat[2]))
                self.interface_data.stacks.append(smd_kat)
        while i < self.interface_data.get_number_slots() - 1:
            self.interface_data.stacks.append(Smd(i, "", ""))
            print('add')
            i += 1
        file_options.close()

    def get_file_name(self, file_path):
        pos = file_path.rfind('\\') + 1
        file_name = file_path[pos:]
        return file_name

    def create_options_file(self):
        file_options_lines = [self.NUMBER_NAME + ") " + str(self.interface_data.device_name),
                              self.NUMBER_SIZE_X + ") " + str(self.interface_data.size_x),
                              self.NUMBER_SIZE_Y + ") " + str(self.interface_data.size_y),
                              self.NUMBER_NUMBER_X + ") " + str(self.interface_data.devices_number_x),
                              self.NUMBER_NUMBER_Y + ") " + str(self.interface_data.devices_number_y),
                              self.NUMBER_SHOW_PLOT + ") " + str(self.interface_data.show_plot),
                              self.NUMBER_SD_CHMT + ") " + str(self.interface_data.copy_to_sd_chmt),
                              self.NUMBER_SD_DISPENSER + ") " + str(self.interface_data.copy_to_sd_dispenser),
                              self.NUMBER_SPLIT_SIZE + ") " + str(self.interface_data.split_size_type)]
        for kat in range(self.interface_data.get_number_slots()):
            str_name = self.interface_data.stacks[kat].pattern_name + ' '
            str_name += self.interface_data.stacks[kat].value + ' '
            str_name += str(self.interface_data.stacks[kat].usage)
            file_options_lines.append("k" + str(kat + 1) + ") " + str_name)

        file_options = open(self.path_to_folder + "optionsSP.txt", 'w')
        for strInput in file_options_lines:
            file_options.write(strInput + "\n")
            # self.PrintCustom(strInput)
        file_options.close()
        # ***********************************************************************

    def convert_pcad_to_files(self):
        self.out_text = ""
        file_name = "input.txt"
        self.path_to_file = self.path_to_folder + file_name
        self.create_chmt_files()

        if self.components:
            self.create_dispenser_files()
            self.print_custom(f"Путь к файлам: {self.path_to_folder}")
            self.print_custom(f"Файл станка CHM-T36:                         "
                              f"{self.get_file_name(self.file_chmt_name)}")
            self.print_custom(f"Файл дозатора (основной):                "
                              f"{self.get_file_name(self.file_dispenser_name_main)}")
            self.print_custom(f"Файл дозатора (настройка начала):  "
                              f"{self.get_file_name(self.file_dispenser_name_control)}")
            self.print_custom(f"Файл дозатора (настройка угла):       "
                              f"{self.get_file_name(self.file_dispenser_name_size)}")

            random.seed()
            if self.interface_data.show_plot:
                self.run_graph_builder()

        self.create_options_file()

    def print_custom(self, param):
        self.out_text += param + "\n"

    def get_print_custom(self):
        return self.out_text


# ***********************************************************************
