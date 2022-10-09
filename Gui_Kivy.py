# ==================================================================
import os
import shutil
from tkinter import filedialog
import tkinter as tk
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
import psutil
# from pywinauto import Application # TODO

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
    bl_dispenser = ObjectProperty()
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

    @staticmethod
    def is_process_exists(class_name):
        pid = 0
        for p in psutil.process_iter(attrs=['pid', 'name']):
            if class_name in (p.info['name']).lower():
                pid = p.info['pid']
        return pid

    def open_pcad_file(self):
        pid = self.is_process_exists('pcad')
        file_opened = False
        if pid != 0:
            print("Окно PCAD найдено, открываю.")
            # app = Application().connect(process=pid) # TODO
            # app.top_window().set_focus()
            file_opened = True
        else:
            print("Окно PCAD не найдено, нужно выбрать файл.")
            file_path = self.call_file_picker("PCAD .pcb file", '.txt')
            print(file_path)
            if file_path.find(".pcb") != -1:
                os.startfile(file_path)
                file_opened = True
        return file_opened

    def input_pcad(self):
        file_opened = self.open_pcad_file()
        if file_opened:
            print("Загружаю данные из PCAD файла.")
            self.converter.input_pcad()
        else:
            print("PCAD файл не загружен.")

    def correct_coords(self):
        file_opened = self.open_pcad_file()
        if file_opened:
            self.converter.correct_coords()
        else:
            print("PCAD файл не загружен.")

    def get_number_coils(self):
        return self.interface_data.NUMBER_COILS

    def get_number_trays(self):
        return self.interface_data.NUMBER_TRAYS

    def get_number_dispenser(self):
        return self.interface_data.NUMBER_DISPENSER

    def print_custom(self, text, end="\n"):
        self.ll_out.text += text + end
        pass

    def refresh_gui_coils_colors(self):
        stack_error = 0
        for kat in self.interface_data.stacks:
            if kat.number > 0:
                self.coil_field_color(kat.number, kat.usage)
            else:
                stack_error = 2

        if stack_error:
            self.print_custom("-------------------------------------------------------------------")
            if stack_error == 1:
                self.print_custom("-------------------- Есть катушки с номером 0 ---------------------")
            if stack_error == 2:
                self.print_custom("------------------ Есть элементы с ручной пайкой ------------------")
            self.print_custom("-------------------------------------------------------------------\n")

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
        for i in range(self.interface_data.get_number_slots()):
            self.ids[str("katPattern" + str(i + 1))].text = self.interface_data.stacks[i].pattern_name
            self.ids[str("katValue" + str(i + 1))].text = self.interface_data.stacks[i].value
        self.refresh_gui_coils_colors()

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
            self.interface_data.stacks[kat].pattern_name = self.ids[str("katPattern" + str(kat + 1))].text
            self.interface_data.stacks[kat].value = self.ids[str("katValue" + str(kat + 1))].text

    def coil_field_color(self, kat_number, usage):
        usage = int(usage)
        if usage == 0:  # full use
            # self.PrintCustom("")
            self.ids["katPattern" + str(kat_number)].background_color = Smd.USAGE_FULL_TEXT_FIELD_COLOR
            self.ids["katValue" + str(kat_number)].background_color = Smd.USAGE_FULL_TEXT_FIELD_COLOR
            self.ids["btddKat" + str(kat_number)].text = Smd.USAGE_FULL_BUTTON_TEXT
        if usage == 1:  # paste only
            # self.PrintCustom("Только паста")
            self.ids["katPattern" + str(kat_number)].background_color = Smd.USAGE_PASTE_TEXT_FIELD_COLOR
            self.ids["katValue" + str(kat_number)].background_color = Smd.USAGE_PASTE_TEXT_FIELD_COLOR
            self.ids["btddKat" + str(kat_number)].text = Smd.USAGE_PASTE_BUTTON_TEXT
        if usage == 2:  # not using
            # self.PrintCustom(" - не используется")
            self.ids["katPattern" + str(kat_number)].background_color = Smd.USAGE_IGNORE_TEXT_FIELD_COLOR
            self.ids["katValue" + str(kat_number)].background_color = Smd.USAGE_IGNORE_TEXT_FIELD_COLOR
            self.ids["btddKat" + str(kat_number)].text = Smd.USAGE_IGNORE_BUTTON_TEXT

    @staticmethod
    def call_file_picker(message, extension):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[(message, extension)])
        return file_path

    def input_saved(self):
        file_path = self.call_file_picker("Input files", '.txt')

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

    def reset_usage(self, usage):
        for kat in range(self.interface_data.get_number_slots() - self.interface_data.NUMBER_DISPENSER):
            self.interface_data.stacks[kat].usage = usage
        self.converter.set_interface_data(self.interface_data)
        self.refresh_gui_coils_colors()

    def calculate_pcad(self):
        self.read_gui()
        self.converter.set_interface_data(self.interface_data)
        self.converter.convert_pcad_to_files()
        self.print_custom(self.converter.get_print_custom())
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
        bubble_button_number = int(data_arr[0])
        kat_number = int(data_arr[1])
        print(data_arr)
        # self.root.ids["bubble_id"].
        # self.cont.remove_widget(self.btn)
        Clock.schedule_once(lambda dt: self.remove_bubble_widget(), 0.1)
        self.interface_data.stacks[kat_number - 1].usage = bubble_button_number
        self.cont.coil_field_color(kat_number, bubble_button_number)

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
        button1 = BubbleButton(text="(П)олный", size_hint=(0.3, 1))
        button1.id = "bb0" + obj.id
        button1.bind(on_press=self.bubble_button_press)
        button2 = BubbleButton(text="(Д)озатор", size_hint=(0.3, 1))
        button2.id = "bb1" + obj.id
        button2.bind(on_press=self.bubble_button_press)
        button3 = BubbleButton(text="(И)гнорировать", size_hint=(0.4, 1))
        button3.id = "bb2" + obj.id
        button3.bind(on_press=self.bubble_button_press)

        # adding buttons to the bubble
        bubble.add_widget(button1)
        bubble.add_widget(button2)
        bubble.add_widget(button3)

        # adding bubble
        self.root.ids[bubble.id] = bubble
        self.cont.fl_main.add_widget(bubble)

    def remove_dropdown_widget(self):
        try:
            self.root.ids["fl_main"].remove_widget(self.root.ids["svDropdown_id"])
            #print("removed")
        except:
            #print("WTF NO ID")
            pass

    def set_pattern(self, obj):
        id_str = obj.id
        # print(id_str)
        id_str = id_str.replace("bpat", "")
        id_str = id_str.replace("katPattern", " ")
        data_arr = id_str.split(" ")
        # pattern_name = int(data_arr[0])
        pattern_name = obj.text
        kat_number = int(data_arr[1])
        self.cont.ids[str("katPattern" + str(kat_number))].text = pattern_name
        # Clock.schedule_once(lambda dt: self.remove_dropdown_widget(), 0.1)
        self.cont.ti_device_name.focus = True
        # self.root.ids["fl_main"].remove_widget(self.root.ids["svDropdown_id"])
        print(kat_number, pattern_name)

    def show_dropdown(self, instance, value):
        if value:
            #print('show')
            sv_dropdown = ScrollView()
            sv_dropdown.id = "svDropdown_id"
            sv_dropdown.bar_width = 6
            sv_dropdown.bar_inactive_color = [0.7, 0.7, 0.7, 0.7]
            sv_dropdown.width = 120
            sv_dropdown.height = 150
            sv_dropdown.size_hint = (None, None)
            top = instance.top - sv_dropdown.height - instance.height
            if top < 0:
                top += sv_dropdown.height
            print(top)
            sv_dropdown.pos = (instance.right - instance.width, top)
            bl_dropdown = BoxLayout()
            bl_dropdown.orientation = "vertical"
            buttons_dd_number = len(Smd.smdParams)
            bl_dropdown.size_hint_min_y = buttons_dd_number * 25
            self.root.ids[sv_dropdown.id] = sv_dropdown

            kat_counter = 1
            for smd_name in Smd.smdParams.keys():
                btn = Button()
                btn.text = smd_name
                btn.id = "bpat" + str(kat_counter) + instance.id
                btn.background_color = [1, 1, 0, 1]
                btn.bind(on_press=self.set_pattern)
                bl_dropdown.add_widget(btn)
                kat_counter += 1
            sv_dropdown.add_widget(bl_dropdown)
            self.cont.fl_main.add_widget(sv_dropdown)
        else:
            self.remove_dropdown_widget()

    @staticmethod
    def box_layout_kat_create():
        bl_kat = BoxLayout()
        bl_kat.orientation = "vertical"
        bl_kat.add_widget(Label(text="| Номер | Режим |       Тип       |    Номинал   |"))
        return bl_kat

    def on_start(self):
        bl_kat_l = self.box_layout_kat_create()
        bl_kat_r = self.box_layout_kat_create()
        number_coils = self.cont.get_number_coils()
        number_trays = self.cont.get_number_trays()
        number_dispenser = self.cont.get_number_dispenser()
        number_smd_inputs = number_coils + number_trays + number_dispenser
        for kat in range(number_smd_inputs):
            bl_kat = BoxLayout()
            bl_kat.orientation = "horizontal"
            bl_kat.padding = (0, 0, 0, 2)
            if kat >= number_trays + number_coils:
                num = kat
                text_str = "Д"
            else:
                num = number_coils + number_trays - kat - 1
                if kat < number_trays:
                    text_str = "Л" + str(3 - kat)
                else:
                    text_str = str(num + 1)

            bl_kat_label = BoxLayout(size_hint=(0.2, 1))
            kat_label = Label(text=text_str, halign="right", valign="middle")
            # kat_label.text_size = bl_kat_label.size
            bl_kat_label.add_widget(kat_label)

            bl_kat_text_input = BoxLayout(size_hint=(0.7, 1))
            kat_text_input_pattern = TextInput(text="Тип")
            kat_text_input_pattern.id = "katPattern" + str(num + 1)
            self.root.ids[kat_text_input_pattern.id] = kat_text_input_pattern
            kat_text_input_pattern.size_hint = (2, 1)
            kat_text_input_pattern.background_color = (1, 1, 0, 1)
            kat_text_input_pattern.bind(focus=self.show_dropdown)
            kat_text_input_value = TextInput(hint_text="Номинал")
            kat_text_input_value.id = "katValue" + str(num + 1)
            self.root.ids[kat_text_input_value.id] = kat_text_input_value
            kat_text_input_value.size_hint = (2.4, 1)
            kat_text_input_value.background_color = (1, 1, 0, 1)
            bl_kat_text_input.add_widget(kat_text_input_pattern)
            bl_kat_text_input.add_widget(kat_text_input_value)

            main_button = Button(text='П', size_hint=(0.1, 1))
            main_button.bind(on_press=self.show_bubble)
            main_button.background_color = (1, 0.6, 0.1, 1)
            main_button.id = "btddKat" + str(num + 1)
            if kat >= number_smd_inputs - number_dispenser:
                main_button.disabled = True
                main_button.text = "Д"
            self.root.ids[main_button.id] = main_button

            bl_kat.add_widget(bl_kat_label)
            bl_kat.add_widget(main_button)
            bl_kat.add_widget(bl_kat_text_input)
            # bl_kat.add_widget(cb_enable)
            if kat < number_coils + number_trays:
                if num % 2:
                    bl_kat_r.add_widget(bl_kat)
                else:
                    bl_kat_l.add_widget(bl_kat)
            else:
                self.cont.bl_dispenser.add_widget(bl_kat)
        kat_text_input = TextInput(hint_text="1")
        kat_text_input.id = "kat"
        self.root.bl_coils.orientation = "horizontal"
        self.cont.bl_coils.add_widget(bl_kat_l)
        self.cont.bl_coils.add_widget(bl_kat_r)

        # self.cont.bl_coils.add_widget(main_button)

        self.converter.read_options_file()
        self.interface_data = self.converter.get_interface_data()

        self.cont.refresh_gui()

    # Основной метод для построения программы
    def build(self):
        # self.load_kv('display.kv')
        self.cont = Container(self.converter)
        return self.cont  # self.cont

# ***********************************************************************
