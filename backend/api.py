import datetime
from flask import Flask, request
from .models.models import SchemaObject, TaskSchema, WhoAmISchema, Task, WhoAmI
from .db_utils import MongoDBHandler, CollectionType
import json
from typing import Dict
from marshmallow import ValidationError
import bson

DEBUG = True

app = Flask(__name__)
create_req_task_schema = TaskSchema(exclude=['_id', 'created_at',
    'detail', 'work_hr_est'], unknown='RAISE')
update_req_task_schema = TaskSchema(unknown='RAISE')
db_handler = MongoDBHandler("mongodb://127.0.0.1:27017")

@app.route("/tasks", methods=['GET', 'POST'])
def tasks():
    # What happens if non GET or POST? TODO: Give it a try
    if request.method == "GET":
        return get_tasks()
    elif request.method == "POST":
        # Get request data, pass to create_task()
        if DEBUG: print("Create task POST request data:", request.data)
        return create_task(request.get_json())

@app.route("/tasks/<string:task_id>", methods=['GET'])
def get_task(task_id: str):
    if DEBUG: print("Getting single task {}".format(task_id))
    return db_handler.find_one(CollectionType.TASK, bson.ObjectId(task_id))

#https://flask.palletsprojects.com/en/1.1.x/quickstart/#variable-rules
@app.route("/tasks/<string:task_id>", methods=['DELETE', 'PATCH'])
def edit_tasks(task_id: str):
    if request.method == "DELETE":
        return delete_task(task_id)
    elif request.method == "PATCH":
        return update_task(task_id, request.get_json())

def delete_task(task_id: str):
    if DEBUG: print("Deleting task:", task_id)
    return ({'message': 'Task deleted'}
            if db_handler.delete(CollectionType.TASK,
                bson.ObjectId(task_id)) == 1
            else ({'message': 'No task found'}, 400))

def update_task(task_id: str, data: Dict):
    if DEBUG: print("Updating task:", task_id)
    try:
        if DEBUG: print("UpdateTask data: ", data)
        new_task = update_req_task_schema.load(data)
    except ValidationError as err: # TODO: See what happens when deserialization fails
        return ({'message': 'Bad request parameters: {}'.format(
            err.messages)}, 400)
    match_count, updated_db_dict = db_handler.update(CollectionType.TASK,
            bson.ObjectId(task_id), new_task)
    return (updated_db_dict if match_count == 1
            else ({'message': '{} not found and not updated'.format(task_id)},
                400))

def get_tasks():
    db_resp = db_handler.find_all(CollectionType.TASK)
    if DEBUG: print("Get tasks db_resp: {}".format(db_resp))
    return db_resp

def create_task(data: Dict):
    # Deserialize request into Task
    try:
        if DEBUG: print("CreateTask data: ", data)
        new_task = create_req_task_schema.load(data) # dict now has creation time
    except ValidationError as err: # TODO: See what happens when deserialization fails
        return ({'message': 'Bad request parameters: {}'.format(
            err.messages)}, 400)
    db_resp = db_handler.create(new_task)
    # Converted to (json, 200 status code) by Flask
    if DEBUG: print("Create task db_resp: {}".format(db_resp))
    return db_resp

# repeat for whoami
