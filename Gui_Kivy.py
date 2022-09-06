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
# ==================================================================
from Solder_Paste import PcadConverter
from Smd_Class import Smd
# ==================================================================


def init_window():
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
    ti_device_name = ObjectProperty()
    cb_chart = ObjectProperty()
    cb_sd_chmt = ObjectProperty()
    cb_sd_dispenser = ObjectProperty()
    bl_coils = ObjectProperty()
    ll_out = ObjectProperty()
    b_input_pcad = ObjectProperty()
    cb_split_size = ObjectProperty()
    b_input_saved = ObjectProperty()

    NUMBER_COILS = 32
    NUMBER_TRAYS = 3

    stacks = []
    device_name = "test"
    size_x = 1
    size_y = 1
    devices_number_x = 1
    devices_number_y = 1
    split_size_type = False
    show_plot = False
    copy_to_sd_chmt = False
    copy_to_sd_dispenser = False
    coils = [" "] * NUMBER_COILS

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
        self.device_name = self.ti_device_name.text
        self.size_x = float(self.ti_size_x.text)
        self.size_y = float(self.ti_size_y.text)
        self.devices_number_x = int(self.ti_devices_number_x.text)
        self.devices_number_y = int(self.ti_devices_number_y.text)
        if self.cb_chart.active:
            self.show_plot = True
        else:
            self.show_plot = False
        if self.cb_sd_chmt.active:
            self.copy_to_sd_chmt = True
        else:
            self.copy_to_sd_chmt = False
        if self.cb_sd_dispenser.active:
            self.copy_to_sd_dispenser = True
        else:
            self.copy_to_sd_dispenser = False
        if self.cb_split_size.active:
            self.split_size_type = True
        else:
            self.split_size_type = False

        if self.devices_number_x == 0:
            self.devices_number_x = 1
        if self.devices_number_y == 0:
            self.devices_number_y = 1
        # print(self.ids)
        for kat in range(self.NUMBER_COILS):
            self.coils[kat] = self.ids[str("kat" + str(kat + 1))].text
            coil = self.coils[kat].split()
            if len(coil) == 2:
                self.stacks[kat].value = coil[1]
                self.stacks[kat].pattern_name = coil[0]
                try:
                    self.height = self.getHeight(self.stacks[kat].pattern_name)
                except:
                    self.height = 0

    def raschet(self):
        self.print_custom("\n")
        self.read_gui()
        PcadConverter.convert_pcad_to_files()


class DisplayApp(App):

    # Создание всех виджетов (объектов)
    def __init__(self):
        super().__init__()

    def on_start(self):
        bl_kat_l = BoxLayout()
        bl_kat_l.orientation = "vertical"
        bl_kat_r = BoxLayout()
        bl_kat_r.orientation = "vertical"
        number_coils = Container.get_number_coils()
        number_trays = Container.get_number_coils()
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

        PcadConverter.read_options_file()

        Container.refresh_gui()

    # Основной метод для построения программы
    def build(self):
        return Container()
