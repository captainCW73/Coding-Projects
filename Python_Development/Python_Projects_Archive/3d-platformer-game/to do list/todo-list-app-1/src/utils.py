def load_tasks(file_path):
    tasks = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                tasks.append(line.strip())
    except FileNotFoundError:
        pass  # If the file doesn't exist, return an empty list
    return tasks

def save_tasks(file_path, tasks):
    with open(file_path, 'w') as file:
        for task in tasks:
            file.write(f"{task}\n")

def validate_task_input(task):
    return isinstance(task, str) and len(task) > 0