# class LoadBalancerRoundRobin():
class LoadBalancer():

	def any_available(self, redis_cache):
		""" returns boolean"""
		all_services = redis_cache.scan_iter("service:*")
		all_services_l = list(all_services)

		print("all services:", all_services_l)
		# return True
		print(len(all_services_l))

		# varianta din laborator pentru circular list
		# print(redis_cache.llen("services"))
		#varianta 2 daca in cache avem doar servicii:
		# print(redis_cache.dbsize())

		return len(all_services_l)>0
		

	def next(self):
		# https://redis.io/commands/rpoplpush
		redis_cache.rpoplpush("services", "services")   

		# circuitbreaker.new()....
		# rpoplpush("services", "services")   



# class LoadBalancer
#   def self.any_available?
#     Cache.current.llen("services") > 0
#   end

#   def self.next
#     CircuitBreaker.new(
#       Cache.current.rpoplpush("services", "services")
#     )
#   end
# end
