class Coil:
    USAGE_FULL = 0
    USAGE_PASTE = 1
    USAGE_IGNORE = 2

    def __init__(self):
        self.pattern_name = ""
        self.value = ""
        self.usage = 0

    def set_string(self, coil_string):
        coil_string_array = coil_string.split(" ")
        self.pattern_name = coil_string_array[0]
        self.value = coil_string_array[1]
        self.usage = int(coil_string_array[2])

    def get_string(self, separator):
        coil_string = self.pattern_name + separator + self.value + separator + str(self.usage)
        return coil_string


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
        self.coils = []
        for i in range(self.NUMBER_COILS):
            self.coils.append(Coil())
