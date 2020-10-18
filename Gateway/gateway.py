#!flask/bin/python
from flask import Flask
from flask import request, abort
import json
import redis
import requests
from loadbalancer import LoadBalancer
from circuitbreaker import CircuitBreaker
from termcolor import colored


app = Flask(__name__)

# redis documentation:
# https://redis-py.readthedocs.io/en/stable/

#json-rpc documentation:
# https://bcb.github.io/jsonrpc/flask

# TODO maybe:
# redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')


# TODO -- QUESTION: why id doesn't clear when running the server??
# redis_cache = redis.Redis(host='localhost', port=6379, db=0)

# redis_cache = redis.Redis(host='172.18.0.1', port=6379, db=0)
# for docker:
redis_cache = redis.Redis(host='redis', port=6379, db=0)
# redis_cache = redis.Redis(host='localhost', port=6379, db=0)
load_balancer = LoadBalancer()

@app.route('/')
def index():
    return "Hello!"
    

@app.route('/<path>', methods=['GET', 'POST'])
def router(path):    
    print(colored("----Request to path:" + path, "yellow"))
    # NOTE: RPC works only with underscore(_) request, but new feature added that gateway can process both _ and - request, so we allow both
    map_service_type_paths = {
        "init-student" : "type1",
        "init_student" : "type1",
        "nota" : "type1",
        "nota-atestare" : "type1",
        "nota_atestare" : "type1",

        "nota-examen" : "type2",
        "nota_examen" : "type2",
        "pune-nota_atestare" : "type2",
        "pune_nota_atestare" : "type2",
        "nota-finala": "type2",
        "nota_finala": "type2",
        "get-all-exam-marks": "type2",
        "get-all-midterm-marks": "type2",
        "s2-nota-atestare": "type2",
        "s2-validate-student-marks":"type2",


        "s2-status": "type2",
        "s1-status": "type1",
        "status" : ""
    }

    allowed_paths = map_service_type_paths.keys()

    if path not in allowed_paths:
        return abort(404, "Page not found")


    service_type = map_service_type_paths[path]

    if path == "s1-status":
        path = "status"
        service_type = "type1"
    elif path == "s2-status":
        path = "status"
        service_type = "type2"

    if not load_balancer.any_available(redis_cache, service_type):
        # TODO: check if 400 bad request is ok or maybe return "no service available" or smth error????
        return abort(400, "No services available")

    if request.method == 'GET':
        data = request.args
    elif request.method == 'POST':
        data = request.data
        # data = request.form
    else:
        data = request.data

    print("DATA", data)

    parameters = {
        # "path": request.path,
        "path": path,
        "parameters": data
    }

    print(colored("parameters:", "magenta"), parameters)

    circuit_breaker = load_balancer.next(redis_cache, service_type)
    service_response = circuit_breaker.request(redis_cache, parameters, request.method)

 
    return service_response


@app.route('/service-register', methods=['GET', 'POST'])
def service_register():
    if request.method == 'GET':
        return abort(405, "Method not allowed. Please make a POST request") #Method not allowed
  
    if request.method == 'POST':
        print(request.data)
        print(request.json)
        print("Service discovered!")

        service_name = request.json["service_name"]
        service_address = request.json["address"]
        service_type = request.json["type"]

        if service_type not in ["type1", "type2"]:
            return {"status":"error", "message": "service_type should be type1 or type2"}

        print(colored("service name:", "red"), service_name)
        print(colored("service address:", "red"), service_address)
        print(colored("service type:", "red"), service_type)
        
        try:
            redis_cache.lpush("services-" + str(service_type), service_address)

            return {"status": "success", "message": "Service registered"}
        except:
            return {"status":"error", "message": "ERROR! Service not registered"}


    return {"status": "error", "message":"Hello! service! You must do a POST request to /service-register to register!"}

    

@app.route('/registered-services')
def get_registered_services():
    result = {}

    l_type1 = redis_cache.lrange('services-type1', 0, -1)
    l_type2 = redis_cache.lrange('services-type2', 0, -1)
    
    result_type1 = [x for x in l_type1]
    result_type2 = [x for x in l_type2]

    return {"registered_services-type1": str(result_type1), "registered_services-type2": str(result_type2)}



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
    