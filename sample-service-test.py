#!flask/bin/python
from flask import Flask
from flask import request, abort
import json
import redis
import requests
from termcolor import colored

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello!"


@app.route('/init-student', methods=['POST'])
def init_student():
    return {"message": "Hello student!"}

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=6008, debug =True)
    app.run(port=6005, debug =True)

    