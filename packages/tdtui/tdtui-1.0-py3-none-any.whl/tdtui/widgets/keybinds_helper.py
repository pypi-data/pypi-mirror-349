import urwid


class Keybind_helper(urwid.Filler):
    def __init__(self, *args):
        self.keybinds_list = urwid.SimpleListWalker([])
        self.keybinds = ["reword: r", "change color: h"]
        for keybind in self.keybinds:
            text = urwid.Text(keybind)
            self.keybinds_list.append(text)
        self.keybind_columns = urwid.Columns(self.keybinds_list)
        super().__init__(*args, body=self.keybind_columns)
