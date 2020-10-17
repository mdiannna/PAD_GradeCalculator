# https://sanic.readthedocs.io/en/latest/
# "Sanic is arguably the most popular and most loved async framework in the Python world. "

from sanic import Sanic
from sanic.response import json

app = Sanic(name='service-sanic1')

@app.route("/")
async def test(request):
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)