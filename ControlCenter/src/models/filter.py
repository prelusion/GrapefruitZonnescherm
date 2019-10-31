from src import mvc


class FilterModel(mvc.Model):
    def __init__(self):
        self.filter_connected = mvc.Observable(self, False)
        self.filter_shutter_up = mvc.Observable(self, False)
        self.filter_shutter_down = mvc.Observable(self, False)
        self.filter_select_all = mvc.Observable(self, False)

    def set_filter_connected(self, boolean):
        self.filter_connected.set(boolean)

    def get_filter_connected(self):
        return self.filter_connected.get()

    def set_filter_shutter_up(self, boolean):
        self.filter_shutter_up.set(boolean)

    def get_filter_shutter_up(self):
        return self.filter_shutter_up.get()

    def set_filter_shutter_down(self, boolean):
        self.filter_shutter_down.set(boolean)

    def get_filter_shutter_down(self):
        return self.filter_shutter_down.get()

    def set_filter_select_all(self, boolean):
        self.filter_select_all.set(boolean)

    def get_filter_select_all(self):
        return self.filter_select_all.get()
