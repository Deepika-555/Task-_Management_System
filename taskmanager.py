import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class User:
    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name

class Task:
    def __init__(self, title, description, due_date=None, assignee=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assignee = assignee
        self.completed = False

class TaskManagementSystem:
    def __init__(self):
        self.users = {}
        self.tasks = {}
        self.logged_in_user = None

    def register_user(self, username, password, name):
        if username in self.users:
            return None  # User already exists
        user = User(username, password, name)
        self.users[username] = user
        return user

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            self.logged_in_user = user
            return user
        else:
            return None

    def logout(self):
        self.logged_in_user = None

    def create_task(self, title, description, due_date=None, assignee=None):
        task = Task(title, description, due_date, assignee)
        self.tasks[title] = task
        return task

    def update_task(self, title, new_title=None, description=None, due_date=None, assignee=None, completed=None):
        task = self.tasks.get(title)
        if task:
            task.title = new_title if new_title is not None else task.title
            task.description = description if description is not None else task.description
            task.due_date = due_date if due_date is not None else task.due_date
            task.assignee = assignee if assignee is not None else task.assignee
            task.completed = completed if completed is not None else task.completed
            return task
        else:
            return None

    def delete_task(self, title):
        if title in self.tasks:
            del self.tasks[title]
            return True
        else:
            return False

    def search_tasks(self, keyword):
        return [task for task in self.tasks.values() if
                keyword.lower() in task.title.lower() or
                keyword.lower() in task.description.lower() or
                (task.assignee and keyword.lower() in task.assignee.name.lower())]

    def filter_tasks(self, completed=None, due_date=None):
        filtered_tasks = list(self.tasks.values())
        if completed is not None:
            filtered_tasks = [task for task in filtered_tasks if task.completed == completed]
        if due_date is not None:
            filtered_tasks = [task for task in filtered_tasks if task.due_date == due_date]
        return filtered_tasks

# GUI Implementation
class TaskManagementGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Management System")
        self.task_system = TaskManagementSystem()

        self.create_login_view()

    def create_login_view(self):
        self.clear_window()

        self.username_label = tk.Label(self.master, text="Username:")
        self.username_entry = tk.Entry(self.master)
        self.password_label = tk.Label(self.master, text="Password:")
        self.password_entry = tk.Entry(self.master, show="*")
        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.register_button = tk.Button(self.master, text="Register", command=self.register)

        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()
        self.register_button.pack()

    def create_main_view(self):
        self.clear_window()

        self.create_task_button = tk.Button(self.master, text="Create Task", command=self.create_task_view)
        self.view_tasks_button = tk.Button(self.master, text="View Tasks", command=self.view_tasks)
        self.logout_button = tk.Button(self.master, text="Logout", command=self.logout)

        self.create_task_button.pack()
        self.view_tasks_button.pack()
        self.logout_button.pack()

    def create_task_view(self):
        self.clear_window()

        self.title_label = tk.Label(self.master, text="Title:")
        self.title_entry = tk.Entry(self.master)
        self.description_label = tk.Label(self.master, text="Description:")
        self.description_entry = tk.Entry(self.master)
        self.due_date_label = tk.Label(self.master, text="Due Date (YYYY-MM-DD):")
        self.due_date_entry = tk.Entry(self.master)
        self.assignee_label = tk.Label(self.master, text="Assignee (Username):")
        self.assignee_entry = tk.Entry(self.master)
        self.create_button = tk.Button(self.master, text="Create Task", command=self.create_task)

        self.title_label.pack()
        self.title_entry.pack()
        self.description_label.pack()
        self.description_entry.pack()
        self.due_date_label.pack()
        self.due_date_entry.pack()
        self.assignee_label.pack()
        self.assignee_entry.pack()
        self.create_button.pack()

    def view_tasks(self):
        self.clear_window()

        self.completed_var = tk.BooleanVar()
        self.completed_var.set(False)
        self.completed_checkbox = tk.Checkbutton(self.master, text="Completed", variable=self.completed_var)

        self.due_date_label = tk.Label(self.master, text="Due Date (YYYY-MM-DD):")
        self.due_date_entry = tk.Entry(self.master)
        self.view_button = tk.Button(self.master, text="View Tasks", command=self.display_tasks)

        self.completed_checkbox.pack()
        self.due_date_label.pack()
        self.due_date_entry.pack()
        self.view_button.pack()

    def display_tasks(self):
        completed = self.completed_var.get()
        due_date_str = self.due_date_entry.get()

        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None
        except ValueError:
            messagebox.showerror("Error", "Invalid due date format. Please use YYYY-MM-DD.")
            return

        filtered_tasks = self.task_system.filter_tasks(completed=completed, due_date=due_date)

        self.clear_window()

        if not filtered_tasks:
            tk.Label(self.master, text="No tasks found.").pack()
        else:
            for task in filtered_tasks:
                tk.Label(self.master, text=f"Title: {task.title}, Description: {task.description}, "
                                           f"Assignee: {task.assignee.name if task.assignee else 'Unassigned'}, "
                                           f"Due Date: {task.due_date}, Completed: {task.completed}").pack()

    def create_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        due_date_str = self.due_date_entry.get()
        assignee_username = self.assignee_entry.get()

        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None
        except ValueError:
            messagebox.showerror("Error", "Invalid due date format. Please use YYYY-MM-DD.")
            return

        assignee = self.task_system.users.get(assignee_username)

        if assignee_username and not assignee:
            messagebox.showerror("Error", f"User with username '{assignee_username}' not found.")
            return

        self.task_system.create_task(title, description, due_date, assignee)
        messagebox.showinfo("Success", "Task created successfully.")

    def update_task_view(self):
        self.clear_window()

        self.title_label = tk.Label(self.master, text="Title:")
        self.title_entry = tk.Entry(self.master)
        self.new_title_label = tk.Label(self.master, text="New Title (optional):")
        self.new_title_entry = tk.Entry(self.master)
        self.description_label = tk.Label(self.master, text="Description:")
        self.description_entry = tk.Entry(self.master)
        self.due_date_label = tk.Label(self.master, text="Due Date (YYYY-MM-DD):")
        self.due_date_entry = tk.Entry(self.master)
        self.assignee_label = tk.Label(self.master, text="Assignee (Username):")
        self.assignee_entry = tk.Entry(self.master)
        self.completed_var = tk.BooleanVar()
        self.completed_var.set(False)
        self.completed_checkbox = tk.Checkbutton(self.master, text="Completed", variable=self.completed_var)
        self.update_button = tk.Button(self.master, text="Update Task", command=self.update_task)

        self.title_label.pack()
        self.title_entry.pack()
        self.new_title_label.pack()
        self.new_title_entry.pack()
        self.description_label.pack()
        self.description_entry.pack()
        self.due_date_label.pack()
        self.due_date_entry.pack()
        self.assignee_label.pack()
        self.assignee_entry.pack()
        self.completed_checkbox.pack()
        self.update_button.pack()

    def update_task(self):
        title = self.title_entry.get()
        new_title = self.new_title_entry.get()
        description = self.description_entry.get()
        due_date_str = self.due_date_entry.get()
        assignee_username = self.assignee_entry.get()
        completed = self.completed_var.get()

        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date() if due_date_str else None
        except ValueError:
            messagebox.showerror("Error", "Invalid due date format. Please use YYYY-MM-DD.")
            return

        assignee = self.task_system.users.get(assignee_username)

        if assignee_username and not assignee:
            messagebox.showerror("Error", f"User with username '{assignee_username}' not found.")
            return

        updated_task = self.task_system.update_task(title, new_title, description, due_date, assignee, completed)

        if updated_task:
            messagebox.showinfo("Success", "Task updated successfully.")
        else:
            messagebox.showerror("Error", "Task not found.")

        self.clear_window()

    def delete_task_view(self):
        self.clear_window()

        self.title_label = tk.Label(self.master, text="Title:")
        self.title_entry = tk.Entry(self.master)
        self.delete_button = tk.Button(self.master, text="Delete Task", command=self.delete_task)

        self.title_label.pack()
        self.title_entry.pack()
        self.delete_button.pack()

    def delete_task(self):
        title = self.title_entry.get()

        if self.task_system.delete_task(title):
            messagebox.showinfo("Success", "Task deleted successfully.")
        else:
            messagebox.showerror("Error", "Task not found.")

        self.clear_window()

    def search_tasks_view(self):
        self.clear_window()

        self.search_label = tk.Label(self.master, text="Search Keyword:")
        self.search_entry = tk.Entry(self.master)
        self.search_button = tk.Button(self.master, text="Search Tasks", command=self.search_tasks)

        self.search_label.pack()
        self.search_entry.pack()
        self.search_button.pack()

    def search_tasks(self):
        keyword = self.search_entry.get()

        if not keyword:
            messagebox.showerror("Error", "Please enter a search keyword.")
            return

        found_tasks = self.task_system.search_tasks(keyword)

        self.clear_window()

        if not found_tasks:
            tk.Label(self.master, text="No tasks found.").pack()
        else:
            for task in found_tasks:
                tk.Label(self.master, text=f"Title: {task.title}, Description: {task.description}, "
                                           f"Assignee: {task.assignee.name if task.assignee else 'Unassigned'}, "
                                           f"Due Date: {task.due_date}, Completed: {task.completed}").pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.task_system.login(username, password)

        if user:
            messagebox.showinfo("Success", f"Logged in as {user.name}.")
            self.create_main_view()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def logout(self):
        self.task_system.logout()
        messagebox.showinfo("Success", "Logged out successfully.")
        self.create_login_view()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return

        user = self.task_system.register_user(username, password, "New User")

        if user:
            messagebox.showinfo("Success", "Registration successful. Please log in.")
        else:
            messagebox.showerror("Error", "Username already exists. Please choose another.")

        self.clear_window()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagementGUI(root)
    root.mainloop()
