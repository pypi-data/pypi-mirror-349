import urwid


class Task_input(urwid.LineBox):
    def __init__(self, *args):
        self.input = urwid.Edit(multiline=False)
        super().__init__(*args, original_widget=self.input, title_align="left")

    def keypress(self, size, key):
        if len(self.input.get_edit_text()) < 30:
            super().keypress(size, key)
