class CheckList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append({"task": task, "completed": False})

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]

    def get_tasks(self):
        return self.tasks

    def format_tasks(self):
        formatted_tasks = []
        for i, task in enumerate(self.tasks):
            checkbox = "[x]" if task["completed"] else "[ ]"
            formatted_tasks.append(f"{checkbox} {task['task']}")
        return formatted_tasks