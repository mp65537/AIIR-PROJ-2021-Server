from enum import Enum
from collections import deque

class TaskManager:
    def __init__(self, root_target, targets_dict):
        self._id_to_task = {}
        self._name_to_task = {}
        self._ready_tasks = deque()
        self._root_task = self._create_tree(
            root_target, None, targets_dict)

    def _create_tree(self, target_name, parent_task, targets_dict):
        existing_task = self._name_to_task.get(target_name, None)
        if existing_task is not None:
            existing_task.depends_on.append(parent_task)
            return existing_task
        task_target = targets_dict["target_name"]
        task_obj = Task(task_target, parent_task)
        self._id_to_task[task_obj.id] = task_obj
        self._name_to_task[target_name] = task_obj
        task_deps = task_obj.deps
        for dep_name in task_target["deps"]:
            task_deps.append(self._create_tree(
                dep_name, task_obj, targets_dict))
            task_obj.counter += 1
        if len(task_deps) == 0:
            self._ready_tasks.append(task_obj)
        return task_obj

    @property
    def all_done(self):
        return (self._root_task.state == TaskState.DONE)

    def take_next(self):
        try:
            next_task = self._ready_tasks.popleft()
        except IndexError:
            return None
        next_task.state = TaskState.IN_PROGRESS
        return next_task.data
        
    def mark_done(self, task_id):
        task_to_mark = self._id_to_task[task_id]
        task_to_mark.state = TaskState.DONE
        for parent_task in task_to_mark.depends_on:
            parent_task.counter -= 1
            if parent_task.counter == 0:
                self._ready_tasks.append(parent_task)

class Task:
    next_task_id = 1

    def __init__(self, target_data, depends_on):
        self.id = type(self).next_task_id
        type(self).next_task_id += 1
        self.name = target_data["name"]
        self.command = target_data["command"]
        self.check_exist = target_data["check_exist"]
        self.depends_on = [] 
        if depends_on is not None:
            self.depends_on.append(depends_on)
        self.deps = []
        self.state = TaskState.WAITING
        self.counter = 0

    @property
    def data(self):
        return {
            "id": self.id,
            "name": self.name,
            "command": self.command,
            "check_exist": self.check_exist,
        }

class TaskState(Enum):
    WAITING = 1
    IN_PROGRESS = 2
    DONE = 3
