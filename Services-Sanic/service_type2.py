################### Service of type 2
# Routes:
# POST /nota-examen { “student”: “NumePrenume1”, “nota”:7}
# GET /nota-examen {"student": "NumePrenume"}
# POST /pune-nota-atestare { “student”: “NumePrenume1”, “nota”: 9, “nr_atestare”}
# GET /nota-finala => {“student”: “NumePrenume1”, “note_atestari”: [“atest1”: nota, “atest2”: “”] “nota_examen” : nota_examen ,“nota_finala”: 9.88} (daca o atestare lipseste, sau examenul, la nota finala ii returneaza eroare)
# GET /status {“student” :”NumePrenume”} => {“status” :”processing}



#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from sanic import response
from sanic_jinja2 import SanicJinja2
from sanic_motor import BaseModel
from models import ExamMark, MidtermMark
from controllers import MarksController
from termcolor import colored

app = Sanic(__name__)

# https://github.com/lixxu/sanic-motor
# https://github.com/lixxu/sanic-motor/blob/master/example/myapp.py

# "mongodb://127.0.0.1:27017"
settings = dict(MOTOR_URI='mongodb://localhost:27017/service2-mongo-students',
                LOGO=None,
                )
app.config.update(settings)

BaseModel.init_app(app)
jinja = SanicJinja2(app, autoescape=True)


# TODO: de pus in models
# class User(BaseModel):
#     __coll__ = 'users'
#     __unique_fields__ = ['name']
#     # __unique_fields__ = ['name, age']   # name and age for unique



@app.route('/')
async def index(request):
    return response.json({"server status": "up and running", "message":"Hello!"})

# # Added new route
# @app.route("/init-student", methods=["POST", "GET"])
# async def init_student(request):
#   if request.method=='POST':
#       student = request.json.get("student", "")
#       st = StudentController()
#       return st.init_student(student)


@app.route("/nota-examen", methods=["POST", "GET"])
async def nota_examen(request):
    
    # curl -d '{"student":"Diana Marusic", "nota": "10"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/nota-examen
    if request.method=='POST':
        student = request.json.get("student", "")
        nota = request.json.get("nota", "")
        # TODO
        await ExamMark.insert_one(dict(student=student, mark=int(nota), status="processing"))

        return response.json({"status": "success", "message": "Exam mark saved successfully"})
    
        # return m.save_exam_mark(student, nota)

    else: #GET
        """
        curl -X GET \
      -H "content-type: application/json" \
      -H "Accept: application/json" \
      -d '{"student":"Diana Marusic"}' \
      "http://127.0.0.1:8000/nota-examen"
      """

        print(colored("request:", "blue"))
        print(request)
        print(colored("request json:", "blue"))
        print(request.json)
        print(colored("-------:", "blue"))

        student = request.json.get("student", "")        

        # exam_mark = await ExamMark.find_one({"student":student}, as_raw=True)
        exam_mark = await ExamMark.find_one({"student":student})
        print(colored("exam mark:", "yellow"), exam_mark)   

        print(colored("exam mark:", "yellow"), exam_mark.mark)   
        if exam_mark:
            return response.json({"status": "success", "student":student, "exam_mark": exam_mark.mark})

        return response.json({"status": "error", "message": "Exam mark not found for student " + student + ". Error"})
        
    return response.json({"status": "TODO"})


# curl -d '{"name":"Diana Marusic", "age": "22"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/new
@app.route("/pune-nota-atestare", methods=["POST"])
async def pune_nota_atestart(request):
    if request.method=="POST":
        student = request.json.get("student", "")
        nota = request.json.get("nota", "")
        nr_atestare = request.json.get("nr_atestare", "")

    # TODO
    return response.json({"status": "TODO"})


@app.route("/nota-finala", methods=["POST"])
async def get_nota_finala(request):
    if request.method=="POST":
        student = request.json.get("student", "")
    

    # TODO
    # return {“student”: “NumePrenume1”, “note_atestari”: [“atest1”: nota, “atest2”: “”] “nota_examen” : nota_examen ,“nota_finala”: 9.88} (daca o atestare lipseste, sau examenul, la nota finala ii returneaza eroare)
    return response.json({"status": "TODO"})


@app.route("/status", methods=["GET"])
async def status(request):
    student = request.json.get("student", "")
    
    # TODO
    return response.json({"status": "TODO"})




if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8000, debug=True)
    # 0.0.0.0 accesibil din retea
    app.run(host='0.0.0.0', port=8000, debug=True)