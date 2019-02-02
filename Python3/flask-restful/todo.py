from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)

api = Api(app)

TODOS = {
    'todo1': {'task': 'Build an API'},
    'todo2': {'task': 'Test it'},
    'todo3': {'task': 'Write Blog'},
}

def abort_if_todo_doesnt_exist(todo_id):
        if todo_id not in TODOS:
            abort(404, message="Todo {} doesn't exist.".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


class Todo(Resource):
    """
    @api {get} /todo/task/<task_id> get todo by id
    @apiVersion 0.1.0
    @apiName GetTodoItem
    @apiGroup Todo
    @apiPermission all
    @apiParam {Number} task_id The todo id.
    @apiExample Example usage:
        https://localhost:5000/v1/todo/task/todo1
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {'task': 'Build an API'}
    """
    """
    @api {get} /todo/<todo_id> get todo by id
    @apiVersion 0.2.0
    @apiName GetTodoItem
    @apiGroup Todo
    @apiPermission all
    @apiParam {Number} todo_id The todo id.
    @apiExample Example usage:
        https://localhost:5000/v1/todo/todo1
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {'task': 'Build an API'}
    """
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]
    """
    @api {delete} /todo/<todo_id> delete todo task by id
    @apiVersion 0.1.0
    @apiName DeleteTodo
    @apiGroup Todo
    @apiPermission admin
    @apiParam {Number} todo_id The todo id.
    @apiExample Example usage:
        https://localhost:5000/v1/todo/todo1
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 204 No Content
    @apiErrorExample Response (example):
        HTTP/1.1 401 Not Authenticated
        {"error": "NoAccessRight"}
    """
    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204
    """
    @api {put} /todo/<todo_id> put a new task
    @apiVersion 0.1.0
    @apiName PutTask
    @apiGroup Todo
    @apiPermission admin
    @apiParam {Number} todo_id The todo id.
    @apiExample Example usage:
        https://localhost:5000/v1/todo/todo1
        {"task": "New Task"}
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 Created 
        {"task": "New Task"}
    """
    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        return task, 201

class TodoList(Resource):
    """
    @api {get} /todos get todolist
    @apiVersion 0.1.0
    @apiName GetTodoList
    @apiGroup TodoList
    @apiPermission all
    @apiExample Example usage:
        https://localhost:5000/v1/todos
    """
    def get(self):
        return TODOS
    """
    @api {post} /todos post todo list
    @apiVersion 0.1.0
    @apiName PostTodoList
    @apiGroup TodoList
    @apiPermission admin
    @apiExample Example usage:
        https://localhost:5000/v1/todo/todo1
        {"task":"New Task"}
    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 Created
        {'task': 'New Task'}
    """
    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == "__main__":
    app.run(debug=True)
