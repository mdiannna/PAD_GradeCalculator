from errors_handling import CustomError, CustomError
import requests
from termcolor import colored
from jsonrpcclient import request as rpc_request
import json

class CircuitBreaker:
    FAILURE_THRESHOLD = 5
    TYPE_REQUESTS = 'RPC'  # this can be 'RPC' or 'HTTP'
    # TYPE_REQUESTS = 'HTTP'  # this can be 'RPC' or 'HTTP'

    # def __init__(address, service_name):
    def __init__(self, address, service_type):
        self.address = address
        self.tripped = False
        self.service_type = service_type


    def request(self, redis_cache, params, method):
        if self.tripped:
            remove_from_cache(redis_cache)
            raise CustomError("Circuit breaker tripped")
            # TODO; check
            return {"status": "error", "message":"Circuit breaker tripped"}

        endpoint = str(self.address.decode("utf-8") ) + str(params["path"]).replace("/", "")
        print(colored("service endpoint:---" + endpoint, "green"))

        # RestClient::Request.execute(params.merge(url:endpoint))
        # rescue errno:ErrorConfused   ???? what is this  QUESTION

        nr_requests_failed = 0
        last_error = ""

        while nr_requests_failed < self.FAILURE_THRESHOLD:
            try:
                if self.TYPE_REQUESTS == 'RPC':
                    print(colored("---RPC", "blue"))
                    route = str(params["path"]).replace("/", "").replace("-", "_")
                    print("-> route:", route)
                    r = rpc_request(str(self.address.decode("utf-8")), route).data.result

                    print(colored("Response from service:----", "green"), r)
                    print(colored("Response from service decoded:----", "green"), json.loads(r))
                    return  json.loads(r)

                elif self.TYPE_REQUESTS == 'HTTP':
                    print("---HTTP")

                    if method=='GET':
                        r = requests.get(endpoint, params=params["parameters"].decode("utf-8"))
                    elif method=='POST':
                        r = requests.post(endpoint, data=params["parameters"].decode("utf-8"))
                    elif method=='PUT':
                        r = requests.put(endpoint, data=params["parameters"].decode("utf-8"))
                    elif method=='DELETE':
                        r = requests.delete(endpoint)

                    print(r)    
                    data = r.json()
                    print(data)
                    print(colored("Response from service:----", "green"), r.json())
                    return r.json()
                
            except Exception as e:

                # TODO: catch specific exceptions
                # QUESTION: why we need redis_key and what is this???
                # result = redis_cache.incr(redis_key) # QUESTION cum incrementam daca redis_key e adresa, deci string??

                nr_requests_failed +=1
                print(colored("----Request failed:----", "red"))
                print(e)
                last_error = str(e)

                # result = Cache.current.incr(redis_key)



        # TODO; check
        # if result > 3: # de ce 3?
        if nr_requests_failed >= self.FAILURE_THRESHOLD:
            self.remove_from_cache(redis_cache)
            self.tripped = True

        return {"status":"error", "message": "Request to service failed", "error":last_error}

    def clear(self, address):
        self.address = None



    # QUESTION - asta e functie sau variabila/valoare & cum incrementam? why we need it?
    def redis_key():
        # TODO : check      
        return "circuit_breaker" + self.address


    def remove_from_cache(self, redis_cache):
        redis_cache.lrem("services", 1, self.address)
        # redis_cache.delete("service:" + self.service_name)

