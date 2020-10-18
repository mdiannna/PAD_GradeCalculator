
from jsonrpcclient import request as rpc_request
# ip = 'http://127.0.0.1:7000/rpc'
ip = 'http://127.0.0.1:8000/rpc'
# route = 'api/rpc/post' + "/" + "init_student"
route = "get_all_midterm_marks"

r = rpc_request(ip, route)
print("---response:", r)

r = r.data.result
print("---response:", r)
# print(json.loads(r))
