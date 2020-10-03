#!flask/bin/python
from flask import Flask
from flask import request, abort
import json
import redis
import requests
from loadbalancer import LoadBalancer

app = Flask(__name__)

# redis documentation:
# https://redis-py.readthedocs.io/en/stable/

# TODO maybe:
# redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')


# TODO -- QUESTION: why id doesn't clear when running the server??
redis_cache = redis.Redis(host='localhost', port=6379, db=0)
loadBalancer = LoadBalancer()

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

    allowed_paths = ["test-service", "calc-midterm", "calc-semester"] #TODO: definit toate allowed path dupa tipurile de servicii (2)

    if path not in allowed_paths:
        return abort(404, "Page not found")


    if not loadBalancer.any_available(redis_cache):
        # TODO: check if 400 bad request is ok or maybe return "no service available" or smth error????
        return abort(400, "No services available")

    # # r = requests.get('https://api.github.com/mdiannna', auth=('user', 'pass'))
    # r = requests.get(service_ip, token=token)
    # print(r.status_code)
    # print(r.headers['content-type'])
    # print(r.text)
    # print(r.json())

    parameters = {
        "request": request.method,
        "path": request.path,
        "parameters": request.data
    }


    # TODO: finish here    QUESTION
    # response = LoadBalancer.next.request(parameters) #TODO python

    # response = LoadBalancer.next.request(
    #     method:  request.request_method,
    #     path:    request.path,
    #     payload: request.body.read
    #   )

    response = "{'response':'test_response lallala'"    
    # json(JSON.parse(response.body))
    return json.dumps(response)


@app.route("/test-400")
def test_400():
    abort(400)

# Example route request load balancing to the service
# @app.route("/nota-teorie/<NumeStudent>", methods=['GET', 'POST'])
@app.route("/nota-teorie/<NumeStudent>", methods=['POST'])
def nota_teorie(NumeStudent):
    # asta daca toate serviciile sunt la fel, noi insa vom avea 2 tipuri diferite de servicii!!!
    # result, status = Make request to loadBalancer.next() + "/nota-teorie/" + NumeStudent
    status = "Error" # ???

    result = {
        "result": "Nota teorie test TODO: finish requests!!!",
        "status": status
    }

    return result


# TODO: delete after testing and clear cache!
@app.route('/test-redis')
def test_redis():
    # redis_cache.set('foo', 'bar')

    # return "Hello, World!" + str(redis_cache.get('foo'))
    return "Hello, World! ------   "  + str(redis_cache.get('service:Service5'))


# @app.route('/service-discovery', methods=['GET', 'POST'])
@app.route('/service-register', methods=['GET', 'POST'])
def service_register():
    if request.method == 'POST':
        print(request.data)
        print(request.json)
        print("Service discovered!")

        service_name = request.json["service_name"]
        service_ip = request.json["ip"]
        # TODO: add service type, and save as "service:servicetype:name"

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

    # TODO: add service type, and save as "service:servicetype:name"
    for key in redis_cache.scan_iter("service:*"):
        value = redis_cache.get(key)
        print(value)
        result[key.decode()] = value.decode()

    return str(result)


if __name__ == '__main__':
    app.run(debug=True)
    