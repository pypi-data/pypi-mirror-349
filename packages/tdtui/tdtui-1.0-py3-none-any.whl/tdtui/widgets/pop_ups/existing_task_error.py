import urwid


class Existing_task_error(urwid.Overlay):
    def __init__(self, main_frame, *args):
        self.main_frame = main_frame
        self.default_text = "This task has already been added"
        self.text = urwid.Text(self.default_text, align="center")
        self.text_filler = urwid.Filler(self.text, valign="middle")
        self.return_text = urwid.Padding(
            urwid.Text("Return: Q", align="right"), right=1
        )
        self.frame = urwid.Frame(self.text_filler, footer=self.return_text)
        self.line_box = urwid.LineBox(self.frame, "Error", title_align="left")
        super().__init__(
            *args,
            top_w=self.line_box,
            bottom_w=self.main_frame.main_layout,
            align="center",
            valign="middle",
            width=("relative", 40),
            height=("relative", 40),
        )
