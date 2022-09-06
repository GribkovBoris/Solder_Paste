# ==================================================================
import os
import shutil
import math
import matplotlib.pyplot as plt
import random
import win32api
import win32file
import ctypes
import tkinter as tk
from tkinter import *
from tkinter import filedialog
# ==================================================================
import Gui_Automizer
import Gui_Kivy
from Smd_Class import Smd


# ***********************************************************************
class Point:
    def __init__(self, x, y, line=0):
        self.x = x
        self.y = y
        self.line = line


# ***********************************************************************
class PcadConverter:
    path_to_folder = os.path.abspath(__file__)
    path_to_folder_output = path_to_folder

    def correct_coords(self):
        point = path_to_folder.rfind("\\")
        this_directory = path_to_folder[:point]
        point = this_directory.rfind("\\")
        this_directory = path_to_folder[:point]

        file_path = call_file_picker()  # call window that allows to pick file
        point = file_path.rfind("/") + 1
        input_file_name = file_path[point:]
        input_file = file_path

        main_file_path = find_file_with_same_name(directory=this_directory, file_name=input_file_name)
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
                input_text = Gui_Automizer.pcad_correct_coords(arr_coords)

                file_input = path_to_folder + "Input.txt"
                file_out = open(file_input, 'w')
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
            self.ti_device_name.text = device_name
            self.ti_size_x.text = str(size_x)
            self.ti_size_y.text = str(size_y)
            shutil.copy(file_path, path_to_folder + "Input.txt")
        pass

    def create_dispenser_files(self):
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
            if qdot.line == self.LINE_START:
                qdot = Point(coords[min_len_index].x, coords[min_len_index].y, coords[min_len_index].line)
                coords_sort.append(qdot)
                coords.pop(min_len_index)
            else:
                if qdot.line == self.LINE_END:
                    qdot = Point(coords[min_len_index - 1].x, coords[min_len_index - 1].y,
                                 coords[min_len_index - 1].line)
                    coords_sort.append(qdot)
                    coords.pop(min_len_index - 1)
        # --------------------------------------------------------------
        board_x = 0
        board_y = 0
        coords_num = len(coords_sort)
        for board_x in range(devices_number_x):
            for board_y in range(devices_number_y):
                if (board_x > 0) or (board_y > 0):
                    for coord in range(coords_num):
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
        file_name_control = path_to_folder_output + device_name + "t.nc"
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
        file_name_main = path_to_folder_output + device_name + ".nc"
        file_code = open(file_name_main, 'w')
        # --------------------------------------------------------------
        file_code.write(";start\n")
        # --------------------------------------------------------------
        for i in range(len(coords_sort)):
            coords_sort[i].x = (coords_sort[i].x * 100)
            coords_sort[i].y = (coords_sort[i].y * 100)
            if (coords_sort[i].line == self.LINE_START) or (coords_sort[i].line == self.LINE_END):
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
        file_name = path_to_folder_output + device_name + "x.nc"
        file_code = open(file_name, 'w')
        # --------------------------------------------------------------
        file_code.write(";start control\n")
        file_code.write(f"d0:x{round(dot_min.x)}y{round(dot_min.y)}z0\n")
        file_code.write(";end\n")
        file_code.write(";m2")
        file_code.close()
        # self.PrintCustom("-------------------------------")

        # --------------------------------------------------------------
        file_input_name = path_to_folder_output + device_name + "input" + str(size_x) + "x" + str(
            size_y) + ".txt"
        file_input = path_to_folder + "input.txt"
        shutil.copy(file_input, file_input_name)
        # --------------------------------------------------------------
        if copy_to_sd_dispenser:
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

    def create_chmt_files(self):
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
            file_chmt_name = path_to_folder_output + device_name + mark_file + ".csv"
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
                stack_error = 2

        if stack_error:
            self.print_custom("-------------------------------------------------------------------")
            if stack_error == 1:
                self.print_custom("-------------------- Есть катушки с номером 0 ---------------------")
            if stack_error == 2:
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
        if copy_to_sd_chmt:
            if len(drives_rem) == 1:
                if not split_size_type:
                    shutil.copy(file_chmt_name, file_sd)
                else:
                    file_chmt_name = path_to_folder_output + device_name + "s" + ".csv"
                    shutil.copy(file_chmt_name, file_sd)
                    file_chmt_name = path_to_folder_output + device_name + "b" + ".csv"
                    shutil.copy(file_chmt_name, file_sd)
            if len(drives_rem) == 0:
                ctypes.windll.user32.MessageBoxW(0, u"Не найдена SD-карта!\nФайл не записан.", u"Ошибка", 0)
            if len(drives_rem) > 1:
                ctypes.windll.user32.MessageBoxW(0, u"Найдено больше одной SD-карты, оставьте нужную!\nФайл не "
                                                    u"записан.", u"Ошибка", 0)

    def read_options_file(self):
        last_slash = path_to_folder.rfind("\\")
        path_to_folder = path_to_folder[:last_slash + 1]
        path_to_folder_output = path_to_folder[:-1]
        last_slash = path_to_folder_output.rfind("\\")
        path_to_folder_output = path_to_folder[:last_slash + 1]
        # Read
        path_to_file = path_to_folder + "optionsSP.txt"
        file_options = open(path_to_file, 'r')
        # Шаблон: х) параметр
        prev_i = 0
        file_options_lines = file_options.readlines()
        for str_input in file_options_lines:
            if str_input[0] == NUMBER_NAME:
                device_name = str_input[3:-1]
            if str_input[0] == NUMBER_SIZE_X:
                size_x = float(str_input[3:-1])
            if str_input[0] == NUMBER_SIZE_Y:
                size_y = float(str_input[3:-1])
            if str_input[0] == NUMBER_NUMBER_X:
                devices_number_x = int(str_input[3:-1])
            if str_input[0] == NUMBER_NUMBER_Y:
                devices_number_y = int(str_input[3:-1])
            if str_input[0] == NUMBER_SPLIT_SIZE:
                if str_input.find("False") != -1:
                    split_size_type = False
                else:
                    split_size_type = True
            if str_input[0] == NUMBER_SHOW_PLOT:
                if str_input.find("False") != -1:
                    show_plot = False
                else:
                    show_plot = True
            if str_input[0] == NUMBER_SD_CHMT:
                if str_input.find("False") != -1:
                    copy_to_sd_chmt = False
                else:
                    copy_to_sd_chmt = True
            if str_input[0] == NUMBER_SD_DISPENSER:
                if str_input.find("False") != -1:
                    copy_to_sd_dispenser = False
                else:
                    copy_to_sd_dispenser = True
            if str_input[0] == "k":
                pos = str_input.find(")")
                i = int(str_input[1:pos]) - 1
                if i > prev_i + 1:
                    j = prev_i + 1
                    while j < i:
                        smd_kat = Smd(j, " ", " ")
                        stacks.append(smd_kat)
                        j += 1
                prev_i = i
                coils[i] = str_input[pos + 2:-1]
                param_kat = coils[i].split()
                if len(param_kat) < 2:
                    param_kat = [" ", " "]
                smd_kat = Smd(i + 1, param_kat[0], param_kat[1])
                stacks.append(smd_kat)
                self.root.ids[str("kat" + str(i + 1))].text = coils[i]
        file_options.close()

    def create_options_file(self):
        file_options_lines = [NUMBER_NAME + ") " + str(self.device_name), NUMBER_SIZE_X + ") " + str(self.size_x),
                              NUMBER_SIZE_Y + ") " + str(self.size_y),
                              NUMBER_NUMBER_X + ") " + str(self.devices_number_x),
                              NUMBER_NUMBER_Y + ") " + str(self.devices_number_y),
                              NUMBER_SHOW_PLOT + ") " + str(self.show_plot),
                              NUMBER_SD_CHMT + ") " + str(self.copy_to_sd_chmt),
                              NUMBER_SD_DISPENSER + ") " + str(self.copy_to_sd_dispenser),
                              NUMBER_SPLIT_SIZE + ") " + str(self.split_size_type)]
        for kat in range(NUMBER_COILS):
            file_options_lines.append("k" + str(kat + 1) + ") " + self.coils[kat])

        file_options = open(self.path_to_folder + "optionsSP.txt", 'w')
        for strInput in file_options_lines:
            file_options.write(strInput + "\n")
            # self.PrintCustom(strInput)
        file_options.close()
        # ***********************************************************************

    def convert_pcad_to_files(self):
        file_name = "input.txt"
        path_to_file = self.path_to_folder + file_name
        self.create_chmt_files()

        if components:
            self.create_dispenser_files()
            self.print_custom(f"Файл для станка CHM-T36:\n     {file_chmt_name}\n")
            self.print_custom(f"Файл для дозатора (калибровочный):\n     {file_name_control}\n")
            self.print_custom(f"Файл для дозатора (основной):\n     {file_name}")
            self.print_custom(f"Файл для дозатора (основной):\n     {file_name}")
            self.print_custom("-------------------------------")
            random.seed()

            if show_plot:
                run_graph_builder()

        self.create_options_file()


# ***********************************************************************
ignore_rotation = False
use_only_one_head = False
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
file_sd = "E:/"
allow_convert = 0
ignore_coef = 0
stack_error = 0
coord_coef = 0.801
x_coef = 1.0
y_coef = 1.0
size_type_small = True
chmtx_coef = 1.0
chmty_coef = 1.0
PI = 3.14159265
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
FIRST_STRING = b'%,\xd4\xad\xb5\xe3\xc6\xab\xd2\xc6,X,Y,'
SECOND_STRING = b'%,\xc1\xcf\xd5\xbb\xc6\xab\xd2\xc6,\xc1\xcf\xd5\xbb\xba\xc5,X,Y,\xbd\xf8\xb8\xf8\xc1\xbf,' \
                b'\xd7\xa2\xca\xcd '
THIRD_STRING = b'%,\xc6\xb4\xb0\xe51,X,Y,'
FOURTH_STRING = b'%,\xcc\xf9\xcd\xb7\xba\xc5,\xc1\xcf\xd5\xbb\xba\xc5,X,Y,\xbd\xc7\xb6\xc8,\xb8\xdf\xb6\xc8,' \
                b'\xcc\xf8\xb9\xfd,\xcb\xd9\xb6\xc8,\xcb\xb5\xc3\xf7,\xd7\xa2\xca\xcd '


# ***********************************************************************
class Component:
    DOT_SMALL = 1
    DOT_MEDIUM = 2
    DOT_BIG = 3
    LINE_START = 8
    LINE_END = 9

    def __init__(self, center, angle, description, comp_type, pattern_name, value):
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.correct_values()
        self.correct_angles(angle)
        self.init_component_parameters()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
        if (ignore_rotation and (self.angle <= 90)) or not ignore_rotation:
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
        for st in self.stacks:
            st_value = st.value
            self.onlyPaste = False
            self.skip = 0
            if st_value.find("*") != -1:
                self.onlyPaste = True
                self.skip = 1
                st_value = st_value.replace("*", "")
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
                    xz = self.center.x + pin.x * math.cos(self.real_angle * PI / 180) - \
                         pin.y * math.sin(self.real_angle * PI / 180)
                    yz = self.center.y + pin.x * math.sin(self.real_angle * PI / 180) + \
                         pin.y * math.cos(self.real_angle * PI / 180)
                    pin.x = xz
                    pin.y = yz


def input_pcad():
    file_input = path_to_folder + "Input.txt"
    file_out = open(file_input, 'w')
    input_text = Gui_Automizer.pcad_reports()
    # input_text = pyperclip.paste()
    input_text = input_text.replace('\n', '')
    print(input_text)
    file_out.write(input_text)
    file_out.close()


def call_file_picker():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("Correct file", ".csv")])


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


def run_graph_builder():
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


# ***********************************************************************
# Запуск проекта
if __name__ == "__main__":
    threadExit = Gui_Automizer.MyThread("exit")
    threadExit.start()
    Gui_Kivy.init_window()
    Gui_Kivy.DisplayApp().run()
# ***********************************************************************
