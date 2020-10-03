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

		# endpoint = self.address + params[:path]
		endpoint = self.address + params["path"]

		# RestClient::Request.execute(params.merge(url:endpoint))
		r = requests.get(endpoint, params["parameters"])
    	
    	# rescue errno:ErrorConfused   ???? what is this

    	result = redis_cache.incr(redis_key)

    	if result > 3:
    		remove_from_cache(redis_cache)
    		self.tripped = True


    def redis_key():
		# TODO : check   	
		return "circuit_breaker" + self.address


	# def remove_from_cache(self, redis_cache):
	def remove_from_cache(redis_cache):
		redis_cache.lrem("services", 1, self.address)

