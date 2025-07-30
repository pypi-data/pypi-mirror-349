import os
from appdirs import user_data_dir
import json
from .widgets.tasks_widgets.task import Task


class Save_state:
    def __init__(self):
        self.app_name = "tdtui"
        self.data_dir = user_data_dir(self.app_name)
        os.makedirs(self.data_dir, exist_ok=True)
        self.save_file = os.path.join(self.data_dir, "tasks.json")
        self.check_exist()
        self.data = self.load()

    def save(self):
        with open(self.save_file, "w") as json_file:
            json.dump(self.data, json_file, indent=4)

    def load(self):
        try:
            with open(self.save_file) as json_file:
                data = json.load(json_file)
                return data
        except json.JSONDecodeError:
            return {"tasks": {}}

    def get_saved_tasks(self, tasks_list, main_frame, names_strs=False):
        if names_strs:
            for task in main_frame.save_state.load()["tasks"].keys():
                tasks_list.append(task)

        else:
            for task_attr in main_frame.save_state.load()["tasks"].items():
                task = Task(task_attr[0], task_attr[1], main_frame)
                tasks_list.append(task.task_color_map)

    def check_exist(self):
        try:
            with open(self.save_file, "x") as json_file:
                pass
        except:
            pass
