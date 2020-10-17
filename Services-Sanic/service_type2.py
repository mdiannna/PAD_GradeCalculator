#!/usr/bin/env python3
# -*- coding: utf-8 -*-


################### Service of type 2
# Routes:
# POST /nota-examen { “student”: “NumePrenume1”, “nota”:7}
# GET /nota-examen {"student": "NumePrenume"}
# POST /pune-nota-atestare { “student”: “NumePrenume1”, “nota”: 9, “nr_atestare”}
# GET /nota-finala => {“student”: “NumePrenume1”, “note_atestari”: [“atest1”: nota, “atest2”: “”] “nota_examen” : nota_examen ,“nota_finala”: 9.88} (daca o atestare lipseste, sau examenul, la nota finala ii returneaza eroare)
# GET /status {“student” :”NumePrenume”} => {“status” :”processing}
#########3


from sanic import Sanic
from sanic import response
from sanic_jinja2 import SanicJinja2
from sanic_motor import BaseModel
from models import ExamMark, MidtermMark
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


@app.route('/')
async def index(request):
    return response.json({"server status": "up and running", "message":"Hello!"})


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

        
    return response.json({"status": "unknown", "message": "Something went wrong"})


# curl -d '{"name":"Diana Marusic", "age": "22"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/new
@app.route("/nota-atestare", methods=["POST"])
async def nota_atestare(request):
    if request.method=="POST":
        student = request.json.get("student", "")
        nota = request.json.get("nota", "")
        nr_atestare = request.json.get("nr_atestare", "")

        try:
            await MidtermMark.insert_one(dict(student=student, mark=int(nota), midterm_nr=nr_atestare, status="processing"))

            return response.json({"status": "success", "message": "Midterm mark saved successfully"})
        except:
            return response.json({"status": "error", "message": "Midterm mark not saved or student " + student + ". Error"})

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
        nr_atestare = request.json.get("nr_atestare", "")

        # exam_mark = await ExamMark.find_one({"student":student}, as_raw=True)
        midterm_mark = await MidtermMark.find_one({"student":student, "midterm_nr": nr_atestare})
        print(colored("midterm mark:", "yellow"), exam_mark)   

        if midterm_mark:
            return response.json({"status": "success", "student":student, "midterm mark": midterm_mark.mark, "midterm nr:": midterm_mark.midterm_nr})

    return response.json({"status": "unknown", "message": "Something went wrong"})


@app.route("/nota-finala", methods=["GET"])
async def get_nota_finala(request):
    student = request.json.get("student", "")
    
    print(colored("Student:" + str(student), "yellow"))
    # midterm_marks = await MidtermMark.find({"student":student})
    # midterm_marks = await MidtermMark.find({"student":student})

    try:
        midterm_marks_cursor = await MidtermMark.find({"student":student})
        # midterm_marks = await midterm_marks_cursor.to_list()

        midterm_marks = midterm_marks.to_list()
        # TODO: finish
    except:
        print(colored("--Error!-- No midterm marks found for student " + student, "red"))
        return response.json({"status": "error", "message":"--Error!-- No midterm marks found for student " + student})

    # print(colored("---Midterm marks:", "blue"), midterm_marks)
    # exam_mark = await ExamMark.find_one({"student":student}).objects
    try:
        exam_mark = await ExamMark.find_one({"student":student})

        print(colored("---Exam mark:", "green"), exam_mark.mark)
        exam_mark = int(exam_mark.mark)
    except:
        print(colored("--Error!-- No exam mark found for student " + student))            
        return response.json({"status": "error", "message":"--Error!-- No exam mark found for student " + student})


    NR_MIDTERMS = 2
    PERCENTAGE_M1 = 30
    PERCENTAGE_M2 = 30
    PERCENTAGE_EXAM = 40
    
    if exam_mark and midterm_marks and (len(midterm_marks) == NR_MIDTERMS):
        final_mark = PERCENTAGE_EXAM / 100.0 * exam_mark + PERCENTAGE_M1 * midterm_marks[0] + PERCENTAGE_M2 * midterm_marks[1]

        return response.json({
            "status": "success", 
            "student":student,
            "note_atestari": midterm_marks, 
            "nota_examen": exam_mark, 
            "nota_finala": final_mark
        })

    elif len(midterm_marks) != NR_MIDTERMS:
        return response.json({
            "status":"error", 
            "message": "Nr of midterms for student " + student + " should be " + str(NR_MIDTERMS) + ", found " + str(len(midterm_marks) )
            }
        )
    else:
        return response.json({"status": "error", "message":"--Error!-- Something went wrong "})

    return response.json({"status": "unknown", "message": "Something went wrong"})
    


@app.route("/status", methods=["GET"])
async def status(request):
    student = request.json.get("student", "")
    
    try:
        nr_midterm_marks_processing = await MidtermMark.count_documents({'status': "processing"})
        nr_exam_marks_processing = await ExamMark.count_documents({'status': "processing"})
        return response.json({
            "status": "success", 
            "nr_midterm_marks_processing":nr_midterm_marks_processing, 
            "nr_exam_marks_processing": nr_exam_marks_processing, 
            "total_processing": nr_midterm_marks_processing + nr_exam_marks_processing
            })
    except:
        return response.json({"status": "error", "message": "Something went wrong"})

    return response.json({"status": "unknown", "message": "Something went wrong"})


#######################
# Additional routes for testing
#######################
# curl -X GET   -H "content-type: application/json" -H "Accept: application/json"  "http://127.0.0.1:8000/get-all-exam-marks"
@app.route('/get-all-exam-marks')
async def get_all_exam_marks(request):
    try:    
        cursor_marks = await ExamMark.find(sort='student')
        marks = cursor_marks.objects
        
        results = {}
        for obj in marks:
            results[obj.student] = obj.mark

        return response.json({"status": "success", "results":results})
    except:
        return response.json({"status": "error", "message": "Something went wrong"})
    return response.json({"status": "unknown", "message": "Something went wrong"})


# curl -X GET   -H "content-type: application/json" -H "Accept: application/json"  "http://127.0.0.1:8000/get-all-midterm-marks"
@app.route('/get-all-midterm-marks')
async def get_all_midterm_marks(request):
    try:    
        cursor_marks = await MidtermMark.find(sort='student')
        marks = cursor_marks.objects
        
        results = {}
        for obj in marks:
            results[obj.student] = {"midterm_nr": obj.midterm_nr, "mark": obj.mark}

        return response.json({"status": "success", "results":results})
    except:
        return response.json({"status": "error", "message": "Something went wrong"})
    return response.json({"status": "unknown", "message": "Something went wrong"})


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8000, debug=True)
    # 0.0.0.0 accesibil din retea
    app.run(host='0.0.0.0', port=8000, debug=True)