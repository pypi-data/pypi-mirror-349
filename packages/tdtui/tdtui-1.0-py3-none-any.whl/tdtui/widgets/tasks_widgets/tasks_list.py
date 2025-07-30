import urwid
from ..tasks_widgets.incompleted_tasks_list import Incompleted_tasks_list
from ..tasks_widgets.completed_tasks_list import Completed_tasks_list


class Tasks_list(urwid.Pile):
    def __init__(self, main_frame, *args):
        self.main_frame = main_frame
        self.incompleted_tasks = Incompleted_tasks_list()
        self.main_frame.save_state.get_saved_tasks(
            self.incompleted_tasks.list_walker, self.main_frame
        )
        self.completed_tasks = Completed_tasks_list()
        self.existing_tasks = []
        self.main_frame.save_state.get_saved_tasks(
            self.existing_tasks, self.main_frame, names_strs=True
        )

        self.with_scrollbar = [self.incompleted_tasks, self.completed_tasks]
        self.without_scrollbar = [
            self.incompleted_tasks.linebox,
            self.completed_tasks.linebox,
        ]
        super().__init__(
            self.without_scrollbar,
            *args,
        )

    def keypress(self, size, key):
        try:
            if key in ("d", "D"):
                focuesd_task = self.get_listwalker()[
                    self.get_focus().list_box.focus_position
                ].base_widget.task
                self.existing_tasks.remove(focuesd_task)
                if self.get_focus() != self.completed_tasks:
                    del self.main_frame.save_state.data["tasks"][focuesd_task]
                    self.main_frame.save_state.save()
                self.get_listwalker().pop(self.get_focus().list_box.focus_position)
                self.auto_focus()
            elif key in ("k", "K", "up"):
                self.focus_previous()
            elif key in ("j", "J", "down"):
                self.focus_next()
            elif key in ("e", "E"):
                if (
                    self.get_focus() == self.incompleted_tasks
                    and len(self.completed_tasks.list_walker) != 0
                ):
                    self.main_frame.set_footer(None)
                    self.set_focus(self.completed_tasks)
                elif len(self.incompleted_tasks.list_walker) != 0:
                    self.main_frame.set_footer(self.main_frame.keybinds_helper)
                    self.set_focus(self.incompleted_tasks)
            elif key == "esc":
                raise urwid.ExitMainLoop()
            else:
                super().keypress(size, key)

        except IndexError:
            pass

    def focus_next(self):
        if self.get_focus().list_box.focus_position < len(self.get_listwalker()) - 1:
            self.get_focus().list_box.focus_position += 1

    def focus_previous(self):
        if self.get_focus().list_box.focus_position > 0:
            self.get_focus().list_box.focus_position -= 1

    def get_listwalker(self, unfocused=False):
        if self.get_focus() == self.incompleted_tasks and not unfocused:
            return self.incompleted_tasks.list_walker
        elif self.get_focus() != self.incompleted_tasks and unfocused:
            return self.incompleted_tasks.list_walker
        elif self.get_focus() == self.completed_tasks and not unfocused:
            return self.completed_tasks.list_walker
        else:
            return self.completed_tasks.list_walker

    def auto_focus(self):
        if (
            len(self.get_listwalker()) == 0
            and len(self.get_listwalker(unfocused=True)) != 0
        ):
            if self.get_unfocused() == self.completed_tasks:
                self.main_frame.set_footer(None)
            else:
                self.main_frame.set_footer(self.main_frame.keybinds_helper)
            self.set_focus(self.get_unfocused())

        elif (
            len(self.get_listwalker()) == 0
            and len(self.get_listwalker(unfocused=True)) == 0
        ):
            self.main_frame.main_layout.base_widget.set_focus(self.main_frame.task_def)

    def get_unfocused(self):
        if self.get_focus() == self.incompleted_tasks:
            return self.completed_tasks
        else:
            return self.incompleted_tasks
