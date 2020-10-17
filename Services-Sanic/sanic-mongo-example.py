#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from sanic import response
from sanic_jinja2 import SanicJinja2
from sanic_motor import BaseModel


app = Sanic(__name__)

# https://github.com/lixxu/sanic-motor
# https://github.com/lixxu/sanic-motor/blob/master/example/myapp.py

# "mongodb://127.0.0.1:27017"
settings = dict(MOTOR_URI='mongodb://localhost:27017/service-mongo-test',
                LOGO=None,
                )
app.config.update(settings)

BaseModel.init_app(app)
jinja = SanicJinja2(app, autoescape=True)


class User(BaseModel):
    __coll__ = 'users'
    __unique_fields__ = ['name']
    # __unique_fields__ = ['name, age']   # name and age for unique


@app.route('/')
async def index(request):
    cur = await User.find(sort='name')
    return jinja.render('index.html', request, users=cur.objects)


# curl -d '{"name":"Diana Marusic", "age": "22"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/new

# @app.route("/new", methods=("GET", "POST"))
@app.route("/new", methods=["POST"])
async def new(request):
    if request.method == "POST":
        print("request!!1")
        # name = request.form.get("name", "").strip().lower()
        name = request.json.get("name", "").strip().lower()
        # age = request.form.get("age", "").strip()
        age = request.json.get("age", "").strip()
        if name:
            is_uniq = await User.is_unique(doc=dict(name=name))
            if is_uniq in (True, None):
                await User.insert_one(dict(name=name, age=int(age)))
                # request["flash"]("User was added successfully", "success")
                return redirect(app.url_for("index"))
            else:
                # request["flash"]("This name was already taken", "error")
                return response.json({"status":"error", "message": "This name was already taken"})

        # request["flash"]("User name is required", "error")
        return response.json({"status":"error", "message": "User name is required"})

    # asta era pentru get cu formular in frontend
    # return jinja.render("form.html", request, user={})
    return response.json({"status": "success", "message": "User created successfully"})




@app.route("/show/<id>")
async def show(request, id):
    # add as_raw = True to get the dict format record
    user_dict = await User.find_one(id, as_raw=True)

    # user = await User.find_one(id)
    return json(dict(user=user_dict))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)