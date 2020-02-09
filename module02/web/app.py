#!flask/bin/python3
# import sys
from flask import Flask, jsonify, request, make_response, url_for

app = Flask(__name__)
print(__name__)

tasks = [
    {
            'id': 0,
            'title': u'Task 00',
            'description': u'Description for the task 00',
            'done': False
    },
    {
            'id': 1,
            'title': u'Task 01',
            'description': u'Description for the task 01',
            'done': True
    },
    {
            'id': 2,
            'title': u'Task 02',
            'description': u'Description for the task 02',
            'done': True
    },
]


@app.route('/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks' : [make_public_task(task) for task in tasks]})

@app.route('/api/v1.0/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if(len(task)) == 0:
        make_response(jsonify({'error': 'Task not found'}), 404)
    return jsonify({'task' : make_public_task(task[0])})

@app.route('/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        make_response(jsonify({'error': 'Unable to add task'}), 400)
    if 'title' in request.json and type(request.json['title']) != 'unicode':
        make_response(jsonify({'error': 'Request error'}), 404)
    if 'description' in request.json and type(request.json['description']) is not 'unicode':
        make_response(jsonify({'error': 'Request error'}), 404)
    if 'done' in request.json and type(request.json['done']) is not bool:
        make_response(jsonify({'error': 'Request error'}), 404)

    task = {
            'id': tasks[-1]['id'] + 1,
            'title': request.json['title'],
            'description': request.json.get('description', ""),
            'done': request.json.get('done', False)
        }
    tasks.append(task)
    return jsonify({'task' : make_public_task(task) }), 201


@app.route('/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if(len(task)) == 0:
        make_response(jsonify({'error': 'Task not found'}), 404)
    tasks.remove(task[0])

    return jsonify({'result' : True, "task":make_public_task(task[0])}), 200


@app.route('/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if(len(task)) == 0:
        make_response(jsonify({'error': 'Task not found'}), 404)
    if not request.json:
        make_response(jsonify({'error': 'Request error'}), 404)
    if 'title' in request.json and type(request.json['title']) != 'unicode':
        make_response(jsonify({'error': 'Request error'}), 404)
    if 'description' in request.json and type(request.json['description']) is not 'unicode':
        make_response(jsonify({'error': 'Request error'}), 404)
    if 'done' in request.json and type(request.json['done']) is not bool:
        make_response(jsonify({'error': 'Request error'}), 404)

    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({"task": make_public_task(task[0])})

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

if __name__ == '__main__':
    app.run(port=5000, debug=True)
