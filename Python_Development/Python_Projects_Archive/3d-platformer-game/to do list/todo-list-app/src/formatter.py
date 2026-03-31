class Formatter:
    def format_task(self, task, completed=False):
        checkbox = "[x]" if completed else "[ ]"
        return f"{checkbox} {task}"

    def format_list(self, tasks):
        formatted_tasks = [self.format_task(task['name'], task.get('completed', False)) for task in tasks]
        return "\n".join(formatted_tasks)