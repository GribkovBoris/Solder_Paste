class InterfaceData:
    NUMBER_COILS = 29
    NUMBER_TRAYS = 3
    NUMBER_DISPENSER = 3

    def get_number_slots(self):
        return self.NUMBER_COILS + self.NUMBER_TRAYS + self.NUMBER_DISPENSER

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
