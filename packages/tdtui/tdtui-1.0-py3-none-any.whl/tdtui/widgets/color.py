import urwid


class Color(urwid.LineBox):
    def __init__(
        self,
        *args,
    ):
        self.colors = [
            "yellow",
            "magenta",
            "cyan",
            "dark_cyan",
            "green",
            "brown",
            "red",
            "blue",
        ]
        self.colors_attrmap = urwid.SimpleListWalker(
            [self.icon_color(color) for color in self.colors]
        )
        self.colors_list_box = urwid.ListBox(self.colors_attrmap)
        self.color_dict = {i: f"task_{self.colors[i]}" for i in range(len(self.colors))}
        super().__init__(
            *args,
            original_widget=self.colors_list_box,
            title_align="left",
        )

    def keypress(self, size, key):
        if key in ("k", "K", "up"):
            self.focus_previous()
        elif key in ("j", "J", "down"):
            self.focus_next()
        else:
            return super().keypress(size, key)

    def focus_next(self):
        if self.colors_list_box.focus_position < len(self.colors_attrmap) - 1:
            self.colors_list_box.focus_position += 1

    def focus_previous(self):
        if self.colors_list_box.focus_position > 0:
            self.colors_list_box.focus_position -= 1

    def icon_color(self, color):
        icon_text = urwid.Text("")
        return urwid.AttrMap(icon_text, f"task_{color}", f"task_{color}_focus")
