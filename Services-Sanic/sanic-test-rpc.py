from sanic import Sanic
from sanic import response
from sanic_jsonrpc import SanicJsonrpc
import json

# documentation:
# https://pypi.org/project/sanic-jsonrpc/

app = Sanic('server')
# jsonrpc = SanicJsonrpc(app, post_route='/api/rpc/post', ws_route='/api/rpc/ws')
jsonrpc = SanicJsonrpc(app, post_route='/rpc', ws_route='/api/rpc/ws')

@jsonrpc
def sub(a: int, b: int) -> int:
    return a - b

@jsonrpc
async def init_student():
	# asa nu merge pentru gateway sa descifreze
    # return response.json({"status": "success", "message": "Init student!"})
    return json.dumps({"status": "success", "message": "Init student!"})
    # return "hello!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)