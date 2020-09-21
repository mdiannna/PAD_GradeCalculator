class LoadBalancer():

	def self.any_available():
		""" returns boolean"""
		return Cache.current.llen("services") > 0

	def self.next():
		# https://redis.io/commands/rpoplpush
		# rpoplpush("services", "services")   

		# circuitbreaker.new()....
		rpoplpush("services", "services")   
