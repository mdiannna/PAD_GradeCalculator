#!flask/bin/python
from flask import Flask
from flask import request, abort
import json

import redis
import requests

app = Flask(__name__)

redis_cache = redis.Redis(host='localhost', port=6379, db=0)


@app.route('/')
def index():
    return "Hello!"
    


# TODO: load balancer etc
@app.route('/<path>')
def router(path):
    """ algorithm:
    0. Check if any services available
    1. round robin or other algo - choose an ip from the services that is ready to take the request
    2. use multiprocessing for this method
    2.  Request to the respective ip service with multiprocessing (first http, them rpc)
    3. Async get response"""
    
    # service_ip = "" #TODO: choose from registered services round robin or other more intelligent
    # token = "SECRET_KEY"


    if not loadBalancer.any_availabel():
        # TODO: check if 400 bad request is ok or maybe return "no service available" or smth error????
        abort(400)

    # # r = requests.get('https://api.github.com/mdiannna', auth=('user', 'pass'))
    # r = requests.get(service_ip, token=token)
    # print(r.status_code)
    # print(r.headers['content-type'])
    # print(r.text)
    # print(r.json())



    return "Path is:" + path


@app.route("/test-400")
def test_400():
    abort(400)

# Example route request load balancing to the service
# @app.route("/nota-teorie/<NumeStudent>", methods=['GET', 'POST'])
@app.route("/nota-teorie/<NumeStudent>", methods=['POST'])
def nota_teorie(NumeStudent):
    # result, status = Make request to loadBalancer.next() + "/nota-teorie/" + NumeStudent
    status = "Error" # ???

    result = {
        "result": "Nota teorie test TODO: finish requests!!!",
        "status": status
    }

    return result



@app.route('/test-redis')
def test_redis():
    redis_cache.set('foo', 'bar')

    return "Hello, World!" + str(redis_cache.get('foo'))


# @app.route('/service-discovery', methods=['GET', 'POST'])
@app.route('/service-register', methods=['GET', 'POST'])
def service_register():
    if request.method == 'POST':
        print(request.data)
        print(request.json)
        print("Service discovered!")

        service_name = request.json["service_name"]
        service_ip = request.json["ip"]

        print("service name:", service_name)
        print("service ip:", service_ip)
        
        try:
            redis_cache.set(str("service:" + service_name), str(service_ip))
            return "Service registered"
        except:
            return "ERROR! Service not registered"


    return "Hello! service! You must do a POST request to /service-discovery to register!"

    

@app.route('/registered-services')
def get_registered_services():
    result = {}

    for key in redis_cache.scan_iter("service:*"):
        value = redis_cache.get(key)
        print(value)
        result[key.decode()] = value.decode()

    return str(result)


if __name__ == '__main__':
    app.run(debug=True)
    