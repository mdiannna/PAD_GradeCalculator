from errors_handling import CustomError, CustomException


def CircuitBreaker():
	FAILURE_THRESHOLD = 3
	# FAILURE_THRESHOLD = 5

	def __init__(address, service_name):
		self.address = address
		self.tripped = False
		self.service_name


	def clear(self, address):
		self.address = None


	def request(params, redis_cache):
		if self.tripped:
			remove_from_cache(redis_cache)
			raise CustomException("Circuit breaker tripped")
			# TODO; check
			return {"status": "error", "Circuit breaker tripped"}

		endpoint = self.address + params["path"]

		# RestClient::Request.execute(params.merge(url:endpoint))
    	# rescue errno:ErrorConfused   ???? what is this  QUESTION

    	nr_requests_failed = 0

    	while nr_requests_failed < self.FAILURE_THRESHOLD:
			try:
				r = requests.get(endpoint, params["parameters"])
				return r
	    	except:
	    		# TODO: catch specific exceptions
	    		# QUESTION: why we need redis_key and what is this???
		    	# result = redis_cache.incr(redis_key) # QUESTION cum incrementam daca redis_key e adresa, deci string??

		    	nr_requests_failed +=1

		# TODO; check
    	# if result > 3: # de ce 3?
    	if nr_requests_failed >= self.FAILURE_THRESHOLD:
    		remove_from_cache(redis_cache)
    		self.tripped = True

    	return ""


    # QUESTION - asta e functie sau variabila/valoare & cum incrementam?
    def redis_key():
		# TODO : check   	
		return "circuit_breaker" + self.address


    # QUESTION - asta e functie sau variabila/valoare & cum incrementam?
	# def remove_from_cache(self, redis_cache):
	def remove_from_cache(self, redis_cache):
		# redis_cache.lrem("services", 1, self.address)
		redis_cache.delete("service:" + self.service_name)

