import uuid

import flask

import pjrpc
from pjrpc.server.integration import flask as integration

app = flask.Flask(__name__)

methods = pjrpc.server.MethodRegistry()


@methods.add
def add_user(user: dict):
    user_id = uuid.uuid4().hex
    flask.current_app.users[user_id] = user

    return {'id': user_id, **user}



@methods.add
def ping():
    return {"message": "ping!"}

@methods.add
def init_student():
    return json.dumps({"message": "hello student!!!"})



json_rpc = integration.JsonRPC('/rpc/')
json_rpc.dispatcher.add_methods(methods)

app.users = {}

json_rpc.init_app(app)

if __name__ == "__main__":
    app.run(port=8080)