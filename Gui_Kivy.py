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
def init_window():
    # Глобальные настройки
    Window.size = (1400, 700)
    Window.top = 100
    Window.left = 100
    Window.clear_color = (255 / 255, 186 / 255, 3 / 255, 1)
    Window.title = "Solder Paste"

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
        global show_plot
        global copy_to_sd_chmt
        global copy_to_sd_dispenser
        global path_to_folder
        global path_to_folderOutput
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

        last_slash = path_to_folder.rfind("\\")
        path_to_folder = path_to_folder[:last_slash + 1]
        path_to_folderOutput = path_to_folder[:-1]
        last_slash = path_to_folderOutput.rfind("\\")
        path_to_folderOutput = path_to_folder[:last_slash + 1]
        # Read
        path_to_file = path_to_folder + "optionsSP.txt"
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
                    show_plot = False
                else:
                    show_plot = True
            if strInput[0] == NUMBER_SD_CHMT:
                if strInput.find("False") != -1:
                    copy_to_sd_chmt = False
                else:
                    copy_to_sd_chmt = True
            if strInput[0] == NUMBER_SD_dispenser:
                if strInput.find("False") != -1:
                    copy_to_sd_dispenser = False
                else:
                    copy_to_sd_dispenser = True
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

        self.root.ti_device_name.text = device_name
        self.root.ti_size_x.text = str(size_x)
        self.root.ti_size_y.text = str(size_y)
        self.root.ti_devices_number_x.text = str(devices_number_x)
        self.root.ti_devices_number_y.text = str(devices_number_y)
        self.root.cb_chart.active = show_plot
        self.root.cb_sd_chmt.active = copy_to_sd_chmt
        self.root.cb_sd_dispenser.active = copy_to_sd_dispenser
        self.root.cb_split_size.active = split_size_type

        # print(self.root.ids)
        # self.root.ll_out.text = "sads"

    # Основной метод для построения программы
    def build(self):
        return Container()
