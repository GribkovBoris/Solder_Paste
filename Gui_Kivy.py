# ==================================================================
# Import kivy
import shutil
from tkinter import filedialog
import tkinter as tk
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
# ==================================================================
import Solder_Paste
from Smd_Class import Smd


# ==================================================================


def init_window():
    # Глобальные настройки
    Window.size = (1400, 700)
    Window.top = 100
    Window.left = 100
    Window.clear_color = (255 / 255, 186 / 255, 3 / 255, 1)
    Window.title = "Solder Paste"


class InterfaceData:
    NUMBER_COILS = 32
    NUMBER_TRAYS = 3

    def __init__(self):
        self.stacks = []
        self.device_name = "test"
        self.size_x = 1
        self.size_y = 1
        self.devices_number_x = 1
        self.devices_number_y = 1
        self.split_size_type = False
        self.show_plot = False
        self.copy_to_sd_chmt = False
        self.copy_to_sd_dispenser = False
        self.coils = [" "] * self.NUMBER_COILS


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

    def __init__(self, conv: Solder_Paste.PcadConverter, **kwargs):
        super().__init__(**kwargs)
        self.converter = conv
        self.interface_data = InterfaceData()
        self.converter.set_interface_data(self.interface_data)

    def get_number_coils(self):
        return self.NUMBER_COILS

    def get_number_trays(self):
        return self.NUMBER_TRAYS

    def print_custom(self, text, end="\n"):
        self.ll_out.text += text + end
        pass

    def refresh_gui(self):
        self.root.ti_device_name.text = self.device_name
        self.root.ti_size_x.text = str(self.size_x)
        self.root.ti_size_y.text = str(self.size_y)
        self.root.ti_devices_number_x.text = str(self.devices_number_x)
        self.root.ti_devices_number_y.text = str(self.devices_number_y)
        self.root.cb_chart.active = self.show_plot
        self.root.cb_sd_chmt.active = self.copy_to_sd_chmt
        self.root.cb_sd_dispenser.active = self.copy_to_sd_dispenser
        self.root.cb_split_size.active = self.split_size_type

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

        if self.devices_number_x == 0:
            self.interface_data.devices_number_x = 1
        if self.devices_number_y == 0:
            self.interface_data.devices_number_y = 1
        # print(self.ids)
        for kat in range(self.NUMBER_COILS):
            self.interface_data.coils[kat] = self.ids[str("kat" + str(kat + 1))].text
            coil = self.interface_data.coils[kat].split()
            if len(coil) == 2:
                self.interface_data.stacks[kat].value = coil[1]
                self.interface_data.stacks[kat].pattern_name = coil[0]
                Smd.get_height(self.interface_data.stacks[kat])

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


class DisplayApp(App):

    # Создание всех виджетов (объектов)
    def __init__(self):
        super().__init__()
        self.converter = Solder_Paste.PcadConverter()
        self.cont = Container(self.converter)

    def on_start(self):
        bl_kat_l = BoxLayout()
        bl_kat_l.orientation = "vertical"
        bl_kat_r = BoxLayout()
        bl_kat_r.orientation = "vertical"
        number_coils = self.cont.get_number_coils()
        number_trays = self.cont.get_number_coils()
        for kat in range(number_coils):
            num = number_coils - kat - 1
            bl_kat = BoxLayout()
            bl_kat.orientation = "horizontal"
            text_str = "№" + str(num + 1)
            if kat < number_trays:
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

        self.converter.read_options_file()

        self.cont.refresh_gui()

    # Основной метод для построения программы
    def build(self):
        return self.cont
