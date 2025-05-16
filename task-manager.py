# task_manager.py
import json
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.filename = "tasks.json"
        self.load_tasks()
    
    def run(self):
        print("🚀 Personal Task Manager")
        while True:
            self.show_menu()
            choice = input("> Choose an option (1-5): ")
            self.handle_choice(choice)
    
    def show_menu(self):
        print("\n" + "="*30)
        print("1. Add New Task")
        print("2. View All Tasks")
        print("3. Mark Task Complete")
        print("4. Delete Task")
        print("5. Save & Exit")
        print("="*30)

    def handle_choice(self, choice):
        actions = {
            "1": self.add_task,
            "2": self.view_tasks,
            "3": self.mark_complete,
            "4": self.delete_task,
            "5": self.save_and_exit
        }
        action = actions.get(choice, self.invalid_choice)
        action()

    def invalid_choice(self):
        print("❌ Invalid option. Please try again.")

    def add_task(self):
        print("\n➕ Add New Task")
        title = input("Title: ")
        description = input("Description: ")
        due_date = self.get_valid_date()
        
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.tasks.append(task)
        print(f"✅ '{title}' added successfully!")

    def get_valid_date(self):
        while True:
            date = input("Due date (YYYY-MM-DD or leave blank): ")
            if not date:
                return None
            try:
                datetime.strptime(date, "%Y-%m-%d")
                return date
            except ValueError:
                print("❌ Invalid format. Use YYYY-MM-DD or leave blank")

    def view_tasks(self):
        if not self.tasks:
            print("\n📭 No tasks found.")
            return
        
        print("\n📋 Your Tasks:")
        for task in self.tasks:
            status = "✓" if task["completed"] else " "
            due = f"(Due: {task['due_date']})" if task["due_date"] else ""
            print(f"{task['id']}. [{status}] {task['title']} {due}")
            if task["description"]:
                print(f"   └─ {task['description']}")

    def mark_complete(self):
        self.view_tasks()
        if not self.tasks:
            return
            
        try:
            task_id = int(input("\nEnter task ID to mark complete: "))
            task = next((t for t in self.tasks if t["id"] == task_id), None)
            
            if task:
                task["completed"] = True
                print(f"✅ '{task['title']}' marked complete!")
            else:
                print("❌ Task not found")
        except ValueError:
            print("❌ Please enter a number")

    def delete_task(self):
        self.view_tasks()
        if not self.tasks:
            return
            
        try:
            task_id = int(input("\nEnter task ID to delete: "))
            task = next((t for t in self.tasks if t["id"] == task_id), None)
            
            if task:
                self.tasks.remove(task)
                # Reassign IDs
                for i, task in enumerate(self.tasks, 1):
                    task["id"] = i
                print(f"🗑️ '{task['title']}' deleted!")
            else:
                print("❌ Task not found")
        except ValueError:
            print("❌ Please enter a number")

    def save_and_exit(self):
        self.save_tasks()
        print("💾 Tasks saved. Goodbye!")
        exit()

    def save_tasks(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving: {e}")

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                self.tasks = json.load(f)
            print(f"📂 Loaded {len(self.tasks)} tasks")
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
        except Exception as e:
            print(f"❌ Error loading: {e}")
            self.tasks = []

if __name__ == "__main__":
    manager = TaskManager()
    manager.run()