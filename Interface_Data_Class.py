
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