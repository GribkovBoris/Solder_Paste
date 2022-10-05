# ==================================================================
# Import kivy
import shutil
from tkinter import filedialog
import tkinter as tk
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
# ==================================================================
from Solder_Paste import PcadConverter
from Smd_Class import Smd
from Interface_Data_Class import InterfaceData
from win32api import GetSystemMetrics


# ==================================================================
def init_window(width, height):
    # Глобальные настройки
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)
    Window.size = (width, height)
    Window.left = (screen_width - width) / 2
    Window.top = (screen_height - height) / 2
    Window.clear_color = (255 / 255, 186 / 255, 3 / 255, 1)
    Window.title = "Solder Paste"


class Container(BoxLayout):
    ti_size_x = ObjectProperty()
    ti_size_y = ObjectProperty()
    ti_devices_number_x = ObjectProperty()
    ti_devices_number_y = ObjectProperty()
    ti_device_name = ObjectProperty()
    cb_chart = ObjectProperty()
    cb_sd_chmt = ObjectProperty()
    cb_sd_dispenser = ObjectProperty()
    bl_coils = ObjectProperty()
    ll_out = ObjectProperty()
    b_input_pcad = ObjectProperty()
    cb_split_size = ObjectProperty()
    b_input_saved = ObjectProperty()
    fl_main = ObjectProperty()

    def __init__(self, conv: PcadConverter, **kwargs):
        super().__init__(**kwargs)
        self.converter = conv
        self.interface_data = InterfaceData()
        self.converter.set_interface_data(self.interface_data)

    def input_pcad(self):
        self.converter.input_pcad()

    def correct_coords(self):
        self.converter.correct_coords()

    def get_number_coils(self):
        return self.interface_data.NUMBER_COILS

    def get_number_trays(self):
        return self.interface_data.NUMBER_TRAYS

    def print_custom(self, text, end="\n"):
        self.ll_out.text += text + end
        pass

    def refresh_gui_coils_colors(self):
        for kat in self.interface_data.stacks:
            if kat.number > 0:
                if kat.value != "":
                    pass
                    # self.PrintCustom(f"Катушка №{kat.number} -\t{kat.patternName}, {kat.value}","")
                else:
                    pass
                    # self.PrintCustom(f"Катушка №{kat.number} -\t{kat.patternName}","")
                flag = 0
                only_dot_flag = False
                for com in self.converter.components:
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
                    self.ids["kat" + str(kat.number)].background_color = [0.7, 0, 0.1, 1]
                if flag == 1:
                    self.ids["kat" + str(kat.number)].background_color = [0, 1, 0, 1]
                if flag == 2:
                    self.ids["kat" + str(kat.number)].background_color = [0.7, 0.6, 0.1, 1]
            else:
                if kat.value != "":
                    pass
                    # self.PrintCustom(f"Вручную -\t{kat.patternName}, {kat.value}")
                else:
                    pass
                    # self.PrintCustom(f"Вручную -\t{kat.patternName}")

    def refresh_gui(self):
        self.ti_device_name.text = self.interface_data.device_name
        self.ti_size_x.text = str(self.interface_data.size_x)
        self.ti_size_y.text = str(self.interface_data.size_y)
        self.ti_devices_number_x.text = str(self.interface_data.devices_number_x)
        self.ti_devices_number_y.text = str(self.interface_data.devices_number_y)
        self.cb_chart.active = self.interface_data.show_plot
        self.cb_sd_chmt.active = self.interface_data.copy_to_sd_chmt
        self.cb_sd_dispenser.active = self.interface_data.copy_to_sd_dispenser
        self.cb_split_size.active = self.interface_data.split_size_type
        for i in range(self.get_number_coils()):
            self.ids[str("kat" + str(i + 1))].text = self.interface_data.coils[i]

    def read_gui(self):
        self.ll_out.text = ""
        self.interface_data.device_name = self.ti_device_name.text
        self.interface_data.size_x = float(self.ti_size_x.text)
        self.interface_data.size_y = float(self.ti_size_y.text)
        self.interface_data.devices_number_x = int(self.ti_devices_number_x.text)
        self.interface_data.devices_number_y = int(self.ti_devices_number_y.text)
        if self.cb_chart.active:
            self.interface_data.show_plot = True
        else:
            self.interface_data.show_plot = False
        if self.cb_sd_chmt.active:
            self.interface_data.copy_to_sd_chmt = True
        else:
            self.interface_data.copy_to_sd_chmt = False
        if self.cb_sd_dispenser.active:
            self.interface_data.copy_to_sd_dispenser = True
        else:
            self.interface_data.copy_to_sd_dispenser = False
        if self.cb_split_size.active:
            self.interface_data.split_size_type = True
        else:
            self.interface_data.split_size_type = False

        if self.interface_data.devices_number_x == 0:
            self.interface_data.devices_number_x = 1
        if self.interface_data.devices_number_y == 0:
            self.interface_data.devices_number_y = 1
        # print(self.ids)
        for kat in range(self.interface_data.NUMBER_COILS):
            self.interface_data.coils[kat] = self.ids[str("kat" + str(kat + 1))].text
            coil = self.interface_data.coils[kat].split()
            if len(coil) == 2:
                self.interface_data.stacks[kat].value = coil[1]
                self.interface_data.stacks[kat].pattern_name = coil[0]
                Smd.get_height(self.interface_data.stacks[kat].pattern_name)

    def coils_fields_color(self):
        stack_error = 0
        # self.PrintCustom(f"Катушки:")
        for kat in self.interface_data.stacks:
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
                for com in self.components:
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
                if flag == 0:  # not using
                    # self.PrintCustom(" - не используется")
                    self.root.ids["kat" + str(kat.number)].background_color = [0.7, 0, 0.1, 1]
                if flag == 1:  # full use
                    # self.PrintCustom("")
                    self.root.ids["kat" + str(kat.number)].background_color = [0, 1, 0, 1]
                if flag == 2:  # paste only
                    # self.PrintCustom("Только паста")
                    self.root.ids["kat" + str(kat.number)].background_color = [0.7, 0.6, 0.1, 1]
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

    def input_saved(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[("Input files", ".txt")])
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
            shutil.copy(file_path, self.converter.path_to_folder + "Input.txt")
        pass

    def calculate_pcad(self):
        self.print_custom("\n")
        self.read_gui()
        self.converter.convert_pcad_to_files()
        self.ll_out.text = '-----------------------\nВывод:\n-----------------------\n\n' + \
                           self.converter.get_print_custom()
        self.refresh_gui_coils_colors()


class DisplayApp(App):

    # Создание всех виджетов (объектов)
    def __init__(self):
        super().__init__()
        self.cont = None
        self.converter = PcadConverter()
        self.interface_data = InterfaceData()
        self.converter.set_interface_data(self.interface_data)

    def remove_bubble_widget(self):
        try:
            self.root.ids["fl_main"].remove_widget(self.root.ids["bubble_id"])
        except:
            pass

    def bubble_button_press(self, obj):
        id_str = obj.id
        id_str = id_str.replace("bb", "")
        id_str = id_str.replace("btddKat", " ")
        data_arr = id_str.split(" ")
        bubble_button_number = data_arr[0]
        kat_number = data_arr[1]
        print(data_arr)
        # self.root.ids["bubble_id"].
        # self.cont.remove_widget(self.btn)
        Clock.schedule_once(lambda dt: self.remove_bubble_widget(), 0.1)
        if bubble_button_number == '1':
            self.cont.ids["kat" + kat_number].background_color = (1, 1, 0, 1)
        if bubble_button_number == '2':
            self.cont.ids["kat" + kat_number].background_color = (0, 0.4, 0, 1)
        if bubble_button_number == '3':
            self.cont.ids["kat" + kat_number].background_color = (0.4, 0.4, 0.4, 1)

    # Defining the function to show the bubble
    def show_bubble(self, obj):
        # Creating bubble
        size_x = 270
        size_y = 60
        self.remove_bubble_widget()
        bubble = Bubble(size_hint=(None, None), size=(size_x, size_y),
                        top=obj.top + size_y / 2 + size_y / 6, right=obj.right + size_x / 2 + size_x / 5)
        bubble.id = "bubble_id"
        bubble.background_color = (1, 1, 1, 1)
        # creating bubble buttons
        button1 = BubbleButton(text="Полный", size_hint=(0.3, 1))
        button1.id = "bb1" + obj.id
        button1.bind(on_press=self.bubble_button_press)
        button2 = BubbleButton(text="Паста", size_hint=(0.3, 1))
        button2.id = "bb2" + obj.id
        button2.bind(on_press=self.bubble_button_press)
        button3 = BubbleButton(text="Игнорировать", size_hint=(0.4, 1))
        button3.id = "bb3" + obj.id
        button3.bind(on_press=self.bubble_button_press)

        # adding buttons to the bubble
        bubble.add_widget(button1)
        bubble.add_widget(button2)
        bubble.add_widget(button3)

        # adding bubble
        self.root.ids[bubble.id] = bubble
        self.cont.fl_main.add_widget(bubble)

    def on_start(self):
        bl_kat_l = BoxLayout()
        bl_kat_l.orientation = "vertical"
        bl_kat_r = BoxLayout()
        bl_kat_r.orientation = "vertical"
        number_coils = self.cont.get_number_coils()
        number_trays = self.cont.get_number_trays()
        for kat in range(number_coils):
            num = number_coils - kat - 1
            bl_kat = BoxLayout()
            bl_kat.orientation = "horizontal"
            bl_kat.padding = (0, 0, 0, 2)
            text_str = "№" + str(num + 1)
            if kat < number_trays:
                text_str = text_str + "(" + str(3 - kat) + ")"
            kat_label = Label(text=text_str)
            kat_text_input = TextInput(hint_text="1", size_hint=(0.9, 1))
            kat_text_input.id = "kat" + str(num + 1)
            self.root.ids[kat_text_input.id] = kat_text_input
            kat_text_input.size_hint = (2, 1)
            kat_text_input.background_color = (1, 1, 0, 1)
            cb_enable = CheckBox(active=True)
            cb_enable.id = "enKat" + str(num + 1)
            cb_enable.color = (1, 0, 1, 1)

            main_button = Button(text='...', size_hint=(0.4, 1))
            main_button.bind(on_press=self.show_bubble)
            main_button.background_color = (1, 0.6, 0.1, 1)
            main_button.id = "btddKat" + str(num + 1)
            self.root.ids[main_button.id] = main_button

            bl_kat.add_widget(kat_label)
            bl_kat.add_widget(main_button)
            bl_kat.add_widget(kat_text_input)
            # bl_kat.add_widget(cb_enable)
            if num % 2:
                bl_kat_r.add_widget(bl_kat)
            else:
                bl_kat_l.add_widget(bl_kat)
        kat_text_input = TextInput(hint_text="1")
        kat_text_input.id = "kat"
        self.root.bl_coils.orientation = "horizontal"
        self.cont.bl_coils.add_widget(bl_kat_l)
        self.cont.bl_coils.add_widget(bl_kat_r)

        # self.cont.bl_coils.add_widget(main_button)

        self.converter.read_options_file()

        self.cont.refresh_gui()

    # Основной метод для построения программы
    def build(self):
        # self.load_kv('display.kv')
        self.cont = Container(self.converter)
        return self.cont  # self.cont
