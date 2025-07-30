import urwid
from ..tasks_widgets.task import Task
from ..color import Color


class Select_color(Color):
    def __init__(
        self,
        main_widget,
        main_frame,
        list_walker,
        task_name,
    ):
        self.main_frame = main_frame
        self.list_walker = list_walker
        self.task_name = task_name
        self.main_widget = main_widget
        super().__init__()
        self.set_title("Set Color")

    def keypress(self, size, key):
        if key == "enter":
            task = Task(
                self.task_name.input.get_edit_text(),
                self.color_dict[self.colors_list_box.focus_position],
                self.main_frame,
            )
            self.main_frame.save_state.data["tasks"][
                self.task_name.input.get_edit_text()
            ] = self.color_dict[self.colors_list_box.focus_position]
            self.main_frame.save_state.save()
            self.set_add_task_mode()
            self.colors_list_box.set_focus(0)
            self.list_walker.append(task.task_color_map)
        else:
            return super().keypress(size, key)

    def set_add_task_mode(self):
        self.main_widget.set_body(self.task_name)
        self.task_name.input.set_edit_text("")
        self.main_frame.set_body(self.main_frame.main_layout)
        self.main_frame.main_layout.base_widget.set_focus(self.main_frame.task_def)
