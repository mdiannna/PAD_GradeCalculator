# QUESTION (pe jumate) e ok sa dau la functii parametri redis_cache? sau cum sa fac global???


# class LoadBalancerRoundRobin(): # TODO: roundrobin pe urma bonus balancing based on service load
# QUESTION:  cum facem load balancerul cu mai multe servicii (1 calculeaza media pe semestru si cealalta etc, dar sunt diferite round robinuri se primeste) ????
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
		

	def next(self, redis_cache):
		# https://redis.io/commands/rpoplpush
		# TODO: schimbat cumva cu cheie valoare

		# circuitbreaker.new()....
		redis_cache.rpoplpush("service", "service")   

		# redis_cache.get()


#   def self.next
#     CircuitBreaker.new(
#       Cache.current.rpoplpush("services", "services")
#     )
#   end
# end


# BONUS: Load Balancer based on service load:
# (ceva cu status - trebuie sa faca request la servicii sa vada statusul lor )
# https://www.nginx.com/resources/glossary/load-balancing/
# o varianta posibila:
# Least Connections – A new request is sent to the server with the fewest current connections to clients. 
#     The relative computing capacity of each server is factored into determining which one has the least connections.
