
from jsonrpcclient import request as rpc_request
ip = 'http://127.0.0.1:7000/rpc'
# route = 'api/rpc/post' + "/" + "init_student"
route = "init_student"

r = rpc_request(ip, route)
print("---response:", r)

r = r.data.result
print("---response:", r)
# print(json.loads(r))
