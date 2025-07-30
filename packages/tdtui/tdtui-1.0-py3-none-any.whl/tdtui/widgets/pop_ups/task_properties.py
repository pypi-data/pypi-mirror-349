import urwid
from ..color import Color
from ..task_input import Task_input


class Task_properties(urwid.Overlay):
    def __init__(self, task, main_frame, mode="color", *args):
        self.focused_task = task
        self.mode = mode
        if self.mode == "color":
            self.propertie = Color()
            self.propertie.set_title("Change Color")
            self.size = {"height": 10, "width": 30}
        elif self.mode == "reword":
            self.propertie = Task_input()
            self.propertie.set_title("Reword")
            self.size = {"height": 3, "width": 50}
        self.main_frame = main_frame

        super().__init__(
            *args,
            bottom_w=self.main_frame.main_layout,
            top_w=self.propertie,
            align="center",
            width=self.size["width"],
            height=self.size["height"],
            valign="middle",
        )

    def keypress(self, size, key):
        if key in ("q", "Q", "esc"):
            self.main_frame.set_body(self.main_frame.main_layout)

        elif key == "enter":
            if self.mode == "color":
                self.focused_task.change_color(
                    self.propertie.color_dict[
                        self.propertie.colors_list_box.focus_position
                    ]
                )
                self.main_frame.set_body(self.main_frame.main_layout)
            elif self.mode == "reword":
                if (
                    self.propertie.input.get_edit_text()
                    not in self.main_frame.tasks_list.existing_tasks
                ):
                    self.focused_task.reword(self.propertie.input.get_edit_text())
                    self.main_frame.set_body(self.main_frame.main_layout)
                else:
                    self.main_frame.existing_task_error.text.set_text(
                        "You can't reword to existing task"
                    )
                    self.main_frame.set_body(self.main_frame.existing_task_error)

        return super().keypress(size, key)
