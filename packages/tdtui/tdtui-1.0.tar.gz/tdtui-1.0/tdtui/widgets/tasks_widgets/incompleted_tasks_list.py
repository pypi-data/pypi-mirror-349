import urwid


class Incompleted_tasks_list(urwid.ScrollBar):
    def __init__(self, *args):
        self.list_walker = urwid.SimpleListWalker([])
        self.list_box = urwid.ListBox(self.list_walker)
        self.linebox = urwid.LineBox(self.list_box, title="Tasks")
        super().__init__(
            self.linebox,
            thumb_char=urwid.ScrollBar.Symbols.DRAWING_HEAVY,
            *args,
        )
