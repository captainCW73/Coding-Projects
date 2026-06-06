# filepath: /todo-list-app/todo-list-app/src/main.py
from checklist import CheckList
from formatter import Formatter

def main():
    task_list = CheckList()
    formatter = Formatter()

    while True:
        print("\nTo-Do List:")
        print(formatter.format_list(task_list.get_tasks()))
        print("\nOptions:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Toggle Task")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            task_name = input("Enter task name: ")
            task_list.add_task(task_name)
        elif choice == '2':
            task_index = int(input("Enter task index to remove: "))
            task_list.remove_task(task_index)
        elif choice == '3':
            task_index = int(input("Enter task index to toggle: "))
            task_list.toggle_task(task_index)
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()