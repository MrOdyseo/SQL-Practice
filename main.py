import sqlite3

class Todo:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.c = self.conn.cursor()
        self.create_task_table()
        
    def create_task_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                     id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     priority INTEGER NOT NULL
                     );''')
    
    def add_task(self):
        while True:
            name = input('Enter task name: ')
            
            if self.find_task(name):
                print("Task already exists")
                continue

            try:
                self.task_name_check(name)
                break
            except ValueError as e:
                print(e)

        while True:
            priority = int(input('Enter priority: '))
            try:
                self.task_prio_check(priority)
                break
            except ValueError as a:
                print(a)    
        
        self.c.execute('INSERT INTO tasks (name, priority) VALUES (?,?)', (name, priority))
        self.conn.commit()

    def task_name_check(self, task):
        if not task or not task.strip():
            raise ValueError("Task name cannot be empty")
        print(f"Task {task} was added.")
        
    def task_prio_check(self, prio):
        if prio < 1:
            raise ValueError("Priority must be higher than 1")
        print(f"Priority {prio} set.")

    def find_task(self, task_name):
        self.c.execute(
            'SELECT name FROM tasks WHERE name = ?',
            (task_name,)
        )

        row = self.c.fetchone()
        return row[0] if row else None
    
    def print_tasks(self):
        self.c.execute('SELECT * FROM tasks')
        rows = self.c.fetchall()
        for row in rows:
            print(row)

    def change_priority(self, old_prio, new_prio):
        self.c.execute(
            'UPDATE tasks SET priority = ? WHERE id = ?',
            (new_prio, old_prio)
        )
        self.conn.commit()

    def delete_task(self, id):
        self.c.execute(
            'DELETE FROM tasks WHERE id = ?',
            (id,)
        )
        self.conn.commit()
    
    def main_Menu(self):
        print("1. Show Tasks\n"
        "2. Add Task\n"
        "3. Change Priority\n"
        "4. Delete Task\n"
        "5. Exit"
        )

        menu_selection = int(input('Enter menu option: '))

        if menu_selection == 1:
            print("\nTasts TO-DO:")
            self.print_tasks()
            print("-------------")
            self.main_Menu()
        elif menu_selection == 2:
            self.add_task()
            print("-------------")
            self.main_Menu()
        elif menu_selection == 3:
            old_prio = int(input("Which priority level would you like to update?: "))
            new_prio = int(input("What should the new priority level be?: "))
            self.change_priority(old_prio, new_prio)
            self.print_tasks()
            print("-------------")
            self.main_Menu()
        elif menu_selection == 4:
            del_id = int(input("Which ID would you like to delete?: "))
            self.delete_task(del_id)
            print("Task has been deleted")
            print("-------------")
            self.main_Menu()
        else:
            exit

app = Todo()
app.main_Menu()

