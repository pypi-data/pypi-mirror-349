import urwid
from .widgets.input_widgets.add_task_field import Add_task_field
from .widgets.tasks_widgets.tasks_list import Tasks_list
from .widgets.pop_ups.existing_task_error import Existing_task_error
from .save_state import Save_state
from .widgets.keybinds_helper import Keybind_helper


class Main_frame(urwid.Frame):
    def __init__(self, *args):
        self.palette = [
            ("task_yellow", "yellow", ""),
            ("task_yellow_focus", "black", "yellow"),
            ("task_blue", "light blue", ""),
            ("task_blue_focus", "black", "light blue"),
            ("task_cyan", "light cyan", ""),
            ("task_cyan_focus", "black", "light cyan"),
            ("task_dark_cyan", "dark cyan", ""),
            ("task_dark_cyan_focus", "black", "dark cyan"),
            ("task_green", "light green", ""),
            ("task_green_focus", "black", "light green"),
            ("task_brown", "brown", ""),
            ("task_brown_focus", "black", "brown"),
            ("task_red", "light red", ""),
            ("task_red_focus", "black", "light red"),
            ("task_magenta", "light magenta", ""),
            ("task_magenta_focus", "black", "light magenta"),
            ("task_completed", "dark gray", ""),
            ("task_completed_focus", "black", "dark gray"),
        ]
        self.save_state = Save_state()
        self.tasks_list = Tasks_list(self)
        self.task_def = Add_task_field(
            self.tasks_list.incompleted_tasks.list_walker, self
        )
        self.main_layout = urwid.Filler(
            urwid.Pile([("fixed", 15, self.tasks_list), ("fixed", 3, self.task_def)])
        )
        self.color_select_layout = urwid.Filler(
            urwid.Pile([("fixed", 15, self.tasks_list), ("fixed", 10, self.task_def)])
        )
        self.existing_task_error = Existing_task_error(self)
        self.keybinds_helper = Keybind_helper()
        super().__init__(self.main_layout, *args)
        self.main_layout.base_widget.set_focus(self.task_def)

    def keypress(self, size, key):
        if key in ("q", "Q") and self.body != self.color_select_layout:
            # that to exit the pop-up menu
            self.set_body(self.main_layout)
        elif key == "tab":
            if self.main_layout.base_widget.get_focus() == self.task_def:
                if len(self.tasks_list.incompleted_tasks.list_walker) != 0:
                    self.set_footer(self.keybinds_helper)
                    self.main_layout.base_widget.set_focus(self.tasks_list)
                    self.tasks_list.widget_list = self.tasks_list.with_scrollbar
                    self.tasks_list.set_focus(self.tasks_list.incompleted_tasks)
                elif len(self.tasks_list.completed_tasks.list_walker) != 0:
                    self.set_footer(None)
                    self.main_layout.base_widget.set_focus(self.tasks_list)
                    self.tasks_list.widget_list = self.tasks_list.with_scrollbar
                    self.tasks_list.set_focus(self.tasks_list.completed_tasks)
            else:
                self.set_footer(None)
                self.main_layout.base_widget.set_focus(self.task_def)
                self.tasks_list.widget_list = self.tasks_list.without_scrollbar
        else:
            return super().keypress(size, key)

    def padding(self, left=5, right=5):
        return urwid.Padding(self, left=left, right=right)


def run_app():
    app = Main_frame()
    loop = urwid.MainLoop(app.padding(), palette=app.palette)
    loop.run()
