#!flask/bin/python
from flask import Flask
from flask import request
import json

import redis

app = Flask(__name__)

# redis_cache = None
redis_cache = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return "Hello!"
    

@app.route('/test-redis')
def test_redis():
    redis_cache.set('foo', 'bar')

    return "Hello, World!" + str(redis_cache.get('foo'))


@app.route('/service-discovery', methods=['GET', 'POST'])
def service_discovery():
    if request.method == 'POST':
        print(request.data)
        print(request.json)
        print("Service discovered!")

        service_name = request.json["service_name"]
        service_ip = request.json["ip"]

        print("service name:", service_name)
        print("service ip:", service_ip)
    
        redis_cache.set(str("service:" + service_name), str(service_ip))


        return "Service registered"

    return "Hello! service! You must do a POST request to /service-discovery to register!"

    

@app.route('/registered-services')
def get_registered_services():
    result = {}
    for key in redis_cache.scan_iter("service:*"):
        value = redis_cache.get(key)
        print(value)
        result[key.decode()] = value.decode()

        # delete the key
        # redis_cache.delete(key)
    return str(result)

if __name__ == '__main__':
    app.run(debug=True)
    