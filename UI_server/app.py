#!flask/bin/python
from flask import Flask
from flask import request, abort, render_template
# import json
# import requests
from termcolor import colored

app = Flask(__name__)


@app.route('/')
def index_frontend():
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug =True)
    # app.run(port=5005, debug =True)

    