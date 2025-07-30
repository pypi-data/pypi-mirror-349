import urwid
from ..pop_ups.task_properties import Task_properties


class Task(urwid.SelectableIcon):
    def __init__(self, task, color, main_frame, *args):
        self.main_frame = main_frame
        self.is_completed = False
        self.task = task
        self.icons = {"completed": "", "not_completed": ""}
        self.color = color
        self.task_color_map = self.set_color(self.color)
        self.task_completed_color_map = urwid.AttrMap(
            self, "task_completed", "task_completed_focus"
        )
        super().__init__(*args, text=f"{self.get_status()} {self.task}")

    def get_status(self):
        if self.is_completed:
            return self.icons["completed"]
        else:
            return self.icons["not_completed"]

    def change_status(self):
        self.is_completed = not self.is_completed
        self.set_text(f"{self.get_status()} {self.task}")
        self.change_group()

    def change_group(self):
        if self.is_completed:
            self.main_frame.tasks_list.completed_tasks.list_walker.append(
                self.task_completed_color_map
            )
            self.main_frame.tasks_list.incompleted_tasks.list_walker.pop(
                self.main_frame.tasks_list.incompleted_tasks.list_box.focus_position
            )
            del self.main_frame.save_state.data["tasks"][self.task]
        else:
            self.main_frame.tasks_list.incompleted_tasks.list_walker.append(
                self.task_color_map
            )
            self.main_frame.tasks_list.completed_tasks.list_walker.pop(
                self.main_frame.tasks_list.completed_tasks.list_box.focus_position
            )
            self.main_frame.save_state.data["tasks"][self.task] = self.color
        self.main_frame.save_state.save()
        self.main_frame.tasks_list.auto_focus()

    def set_color(self, color):
        return urwid.AttrMap(self, color, f"{color}_focus")

    def change_color(self, color):
        self.task_color_map = self.set_color(color)
        self.color = color
        self.main_frame.tasks_list.incompleted_tasks.list_walker.insert(
            self.main_frame.tasks_list.incompleted_tasks.list_box.focus_position + 1,
            self.task_color_map,
        )
        self.main_frame.tasks_list.incompleted_tasks.list_walker.pop(
            self.main_frame.tasks_list.incompleted_tasks.list_box.focus_position
        )
        self.main_frame.save_state.data["tasks"][self.task] = color
        self.main_frame.save_state.save()

    def reword(self, task):
        del self.main_frame.save_state.data["tasks"][self.task]
        self.main_frame.tasks_list.existing_tasks.remove(self.task)
        self.task = task
        self.set_text(f"{self.get_status()} {self.task}")
        self.main_frame.tasks_list.existing_tasks.append(self.task)
        self.main_frame.save_state.data["tasks"][self.task] = self.color
        self.main_frame.save_state.save()

    def get_color(self):
        return self.color

    def keypress(self, size, key):
        if key == "enter":
            self.change_status()

        elif key in ("h", "H"):
            if not self.is_completed:
                properties = Task_properties(self, self.main_frame)
                self.main_frame.set_body(properties)

        elif key in ("r", "R"):
            if not self.is_completed:
                properties = Task_properties(self, self.main_frame, mode="reword")
                self.main_frame.set_body(properties)

        return super().keypress(size, key)
