from errors_handling import CustomError, CustomException


def CircuitBreaker():
	def __init__(address):
		self.address = address
		self.tripped = False


	def clear(self, address):
		self.address = None


	def request(params, redis_cache):
		if self.tripped:
			remove_from_cache(redis_cache)
			raise CustomException("Circuit breaker tripped")

		endpoint = self.address + params["path"]

		# RestClient::Request.execute(params.merge(url:endpoint))
		r = requests.get(endpoint, params["parameters"])
    	
    	# rescue errno:ErrorConfused   ???? what is this  QUESTION

    	result = redis_cache.incr(redis_key) # QUESTION cum incrementam daca redis_key e adresa, deci string??

    	if result > 3: # de ce 3?
    		remove_from_cache(redis_cache)
    		self.tripped = True


    # QUESTION - asta e functie sau variabila/valoare & cum incrementam?
    def redis_key():
		# TODO : check   	
		return "circuit_breaker" + self.address


    # QUESTION - asta e functie sau variabila/valoare & cum incrementam?
	# def remove_from_cache(self, redis_cache):
	def remove_from_cache(redis_cache):
		redis_cache.lrem("services", 1, self.address)

