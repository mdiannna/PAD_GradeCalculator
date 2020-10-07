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

# TODO maybe:
# redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')


# TODO -- QUESTION: why id doesn't clear when running the server??
redis_cache = redis.Redis(host='localhost', port=6379, db=0)
load_balancer = LoadBalancer()

@app.route('/')
def index():
    return "Hello!"
    

# TODO: load balancer etc
@app.route('/<path>', methods=['GET', 'POST'])
def router(path):
    """ algorithm:
    0. Check if any services available
    1. round robin or other algo - choose an ip from the services that is ready to take the request
    2. use multiprocessing for this method
    2.  Request to the respective ip service with multiprocessing (first http, them rpc)
    3. Async get response"""
    
    # service_ip = "" #TODO: choose from registered services round robin or other more intelligent
    # token = "SECRET_KEY"
 

    map_service_type_paths = {
        "init-student" : "type1",
        "nota" : "type1",
        "nota-atestare" : "type1",

        "nota-examen" : "type2",
        "pune-nota-atestare" : "type2",
        "nota-finala": "type2"
    }

    # allowed_paths = ["test-service", "calc-midterm", "calc-semester"] #TODO: definit toate allowed path dupa tipurile de servicii (2) ???  sau alta metoda???
    allowed_paths = map_service_type_paths.keys()

    if path not in allowed_paths:
        return abort(404, "Page not found")


    service_type = map_service_type_paths[path]

    if not load_balancer.any_available(redis_cache, service_type):
        # TODO: check if 400 bad request is ok or maybe return "no service available" or smth error????
        return abort(400, "No services available")

    # # r = requests.get('https://api.github.com/mdiannna', auth=('user', 'pass'))
    # r = requests.get(service_ip, token=token)
    # print(r.status_code)
    # print(r.headers['content-type'])
    # print(r.text)
    # print(r.json())

    parameters = {
        "path": request.path,
        "parameters": request.data
    }


    # TODO: finish here    QUESTION
    # response = LoadBalancer.next.request(parameters) #TODO python
    print(colored("parameters:", "magenta"), parameters)

    circuit_breaker = load_balancer.next(redis_cache, service_type)
    service_response = circuit_breaker.request(redis_cache, parameters, request.method)
    # response = LoadBalancer.next(service_type).request(parameters) #TODO python

    # response = LoadBalancer.next.request(
    #     method:  request.request_method,
    #     path:    request.path,
    #     payload: request.body.read
    #   )

    response = {'response':service_response, "service_type":service_type, "path":path}
    # json(JSON.parse(response.body))
    # return json.dumps(response)
    return response


@app.route("/test-400")
def test_400():
    abort(400)


# # Example route request load balancing to the service
# # @app.route("/nota-teorie/<NumeStudent>", methods=['GET', 'POST'])
# @app.route("/nota-teorie/<NumeStudent>", methods=['POST'])
# def nota_teorie(NumeStudent):
#     # asta daca toate serviciile sunt la fel, noi insa vom avea 2 tipuri diferite de servicii!!!
#     # result, status = Make request to load_balancer.next() + "/nota-teorie/" + NumeStudent
#     status = "Error" # ???

#     result = {
#         "result": "Nota teorie test TODO: finish requests!!!",
#         "status": status
#     }

#     return result


# TODO: delete after testing and clear cache!
@app.route('/test-redis')
def test_redis():
    # redis_cache.set('foo', 'bar')

    # return "Hello, World!" + str(redis_cache.get('foo'))
    return "Hello, World! ------   "  + str(redis_cache.get('service:Service5'))


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
        # TODO: add service type, and save as "service:servicetype:name"

        print(colored("service name:", "red"), service_name)
        print(colored("service address:", "red"), service_address)
        print(colored("service type:", "red"), service_type)
        
        try:
            # redis_cache.set(str("service:" + service_name), str(service_ip))
            redis_cache.lpush("services", service_address)
            print("yes!")
            return {"status": "success", "message": "Service registered"}
        except:
            return {"status":"error", "message": "ERROR! Service not registered"}


    return {"status": "error", "message":"Hello! service! You must do a POST request to /service-register to register!"}

    

@app.route('/registered-services')
def get_registered_services():
    result = {}

    # # TODO: add service type, and save as "service:servicetype:name"
    # for key in redis_cache.scan_iter("service:*"):
    #     value = redis_cache.get(key)
    #     print(value)
    #     result[key.decode()] = value.decode()


    l = redis_cache.lrange('services', 0, -1)
    result = [x for x in l]
    # for x in l:
    #   print x
    return str(result)


if __name__ == '__main__':
    app.run(debug=True)
    