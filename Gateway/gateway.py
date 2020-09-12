#!flask/bin/python
from flask import Flask

import redis

app = Flask(__name__)


@app.route('/')
def index():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')

    return "Hello, World!" + str(r.get('foo'))



if __name__ == '__main__':
    app.run(debug=True)