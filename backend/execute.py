# Импортируем библиотеку, соответствующую типу нашей базы данных
import sqlite3 as sql
from base import all_todos
# Создаем соединение с нашей базой данных
conn = sql.connect('dataBase.sqlite')
# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cursor = conn.cursor()
# Делаем SELECT запрос к базе данных, используя обычный SQL-синтаксис
cursor.execute("SELECT todo FROM todos ORDER BY todo")

# Получаем результат сделанного запроса
tasks = cursor.fetchall()

a = [str(item) for sub in tasks for item in sub]

class TodoItem:
    all_todos
    def __init__(self, description, unique_id):
        self.description = description
        self.is_completed = False
        self.uid = unique_id
        super(TodoItem, self).__init__()

    def __str__(self):
        return self.description.lower()

    def to_dict(self):
        return {
            "description": self.description,
            "is_completed": self.is_completed,
            "uid": self.uid
        }

tasks_db ={
uid: TodoItem(desc, uid)
    for uid, desc in enumerate(
        start=1,
        iterable=a,
    )
}

# Не забываем закрыть соединение с базой данных
conn.close()


# deleted_todo = session.query(all_todos).filter(all_todos.c.id==uid)
#         deleted_todo.delete(synchronize_session=False)
#         session.commit()

# deleted_todo=all_todos.delete(all_todos.c.id== uid, synchronize_session='fetch')
#         engine.execute(deleted_todo)
#         session.commit()