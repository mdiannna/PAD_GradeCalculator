from errors_handling import CustomError, CustomError
import requests
from termcolor import colored

class CircuitBreaker:
    # FAILURE_THRESHOLD = 3
    FAILURE_THRESHOLD = 5

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

        while nr_requests_failed < self.FAILURE_THRESHOLD:
            try:
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

                # result = Cache.current.incr(redis_key)



        # TODO; check
        # if result > 3: # de ce 3?
        if nr_requests_failed >= self.FAILURE_THRESHOLD:
            self.remove_from_cache(redis_cache)
            self.tripped = True

        return {"status":"error", "message": "Request to service failed"}

    def clear(self, address):
        self.address = None



    # QUESTION - asta e functie sau variabila/valoare & cum incrementam?
    def redis_key():
        # TODO : check      
        return "circuit_breaker" + self.address


    # QUESTION - asta e functie sau variabila/valoare & cum incrementam?
    # def remove_from_cache(self, redis_cache):
    def remove_from_cache(self, redis_cache):
        redis_cache.lrem("services", 1, self.address)
        # redis_cache.delete("service:" + self.service_name)

