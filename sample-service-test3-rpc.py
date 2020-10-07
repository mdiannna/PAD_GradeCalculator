#!flask/bin/python
from flask import Flask
from flask import request, abort
import json
import redis
import requests
from termcolor import colored
from jsonrpcserver import method, dispatch


# json rpc documentation:
# https://bcb.github.io/jsonrpc/flask

app = Flask(__name__)


@method
def ping():
    return {"message": "ping!"}

@method
def init_student():
    return {"message": "hello student!!!"}


@app.route("/", methods=["POST"])
def index():
    req = request.get_data().decode()
    response = dispatch(req)
    return Response(str(response), response.http_status, mimetype="application/json")



# @app.route('/')
# def index():
#     return "Hello!"




# @app.route('/init-student', methods=['POST'])
# def init_student():
#     return {"message": "Hello student!"}

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=6008, debug =True)
    app.run(port=6003, debug =True)

    