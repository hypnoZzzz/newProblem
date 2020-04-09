import bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors
from execute import TodoItem, tasks_db, cursor
from base import all_todos, engine, session

app = bottle.Bottle()


@enable_cors
@app.route("/api/tasks/", method=["GET", "POST"])
def add_task():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    if bottle.request.method == 'GET':
        tasks = [task.to_dict() for task in tasks_db.values()]
        return {"tasks": tasks}
    elif bottle.request.method == "POST":
        desc = bottle.request.json['description']
        is_completed = bottle.request.json.get('is_completed', False)
        if len(desc) > 0:
            new_uid = max(tasks_db.keys()) + 1
            t = TodoItem(desc, new_uid)
            t.is_completed = is_completed
            tasks_db[new_uid] = t
            insert_todo = all_todos.insert().values(todo=desc)
            engine.execute(insert_todo)

        return "OK"


@bottle.route("/api/delete/<uid:int>")
def api_delete(uid):
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    tasks_db.pop(uid)
    return "Ok"


@bottle.route("/api/complete/<uid:int>")
def api_complete(uid):
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    tasks_db[uid].is_completed = True
    return "Ok"


@enable_cors
@app.route("/api/tasks/<uid:int>", method=["GET", "PUT", "DELETE"])
def show_or_modify_task(uid):
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    if bottle.request.method == "GET":
        return tasks_db[uid].to_dict()
    elif bottle.request.method == "PUT":
        if "description" in bottle.request.json:
            tasks_db[uid].description = bottle.request.json['description']
        if "is_completed" in bottle.request.json:
            tasks_db[uid].is_completed = bottle.request.json['is_completed']
        return f"Modified task {uid}"
    elif bottle.request.method == "DELETE":
        tasks_db.pop(uid)
        deleted_todo = session.query(all_todos.c.id==uid).filter(all_todos.c.id==uid)
        deleted_todo.delete(synchronize_session=False)
        session.commit()
        return 'Ok'
    return f"Deleted task {uid}"

# @bottle.route("/api/tasks/<uid:int>", method=["DELETE"])
# def deleted_task(uid):
#     bottle.response.headers['Access-Control-Allow-Origin'] = '*'
#
#     deleted_todo = session.query(all_todos).filter(all_todos.c.id == uid)
#     deleted_todo.delete(synchronize_session=False)
#     session.commit()
#     return "Ok"

app.install(CorsPlugin(origins=['http://localhost:8000']))

if __name__ == "__main__":
    bottle.run(app, host="localhost", port=8081)
