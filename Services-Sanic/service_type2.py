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

from sanic_jsonrpc import SanicJsonrpc
import json


app = Sanic(__name__)

# documentation:
# https://github.com/lixxu/sanic-motor
# https://github.com/lixxu/sanic-motor/blob/master/example/myapp.py

# tutorial to delete database;
# https://www.tutorialkart.com/mongodb/mongodb-delete-database/

# "mongodb://127.0.0.1:27017"
settings = dict(MOTOR_URI='mongodb://localhost:27017/service2-mongo-students',
                LOGO=None,
                )
app.config.update(settings)

BaseModel.init_app(app)
jinja = SanicJinja2(app, autoescape=True)
jsonrpc = SanicJsonrpc(app, post_route='/rpc', ws_route='/api/rpc/ws')


@app.route('/')
async def index(request):
    return response.json({"server status": "up and running", "message":"Hello!"})


@app.route("/nota-examen", methods=["POST", "GET"])
async def nota_examen(request):
    
    # curl -d '{"student":"Diana Marusic", "nota": "10"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/nota-examen
    if request.method=='POST':
        student = request.args.get("student", "")
        nota = request.args.get("nota", "")

        is_uniq = await ExamMark.is_unique(doc=dict(student=student))
        
        if is_uniq in (True, None):
            await ExamMark.insert_one(dict(student=student, mark=int(nota), status="processing"))

            return response.json({"status": "success", "message": "Exam mark saved successfully"})
        else:
            return response.json({"status": "error", "message": "This student already has exam mark!"})        
        
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

        student = request.args.get("student", "")        

        # exam_mark = await ExamMark.find_one({"student":student}, as_raw=True)
        exam_mark = await ExamMark.find_one({"student":student})
        print(colored("exam mark:", "yellow"), exam_mark)   

        print(colored("exam mark:", "yellow"), exam_mark.mark)   
        if exam_mark:
            return response.json({"status": "success", "student":student, "exam_mark": exam_mark.mark})

        return response.json({"status": "error", "message": "Exam mark not found for student " + student + ". Error"})

        
    return response.json({"status": "unknown", "message": "Something went wrong"})


# curl -d '{"name":"Diana Marusic", "age": "22"}' -H 'Content-Type: application/json' http://127.0.0.1:8000/new
@app.route("/s2-nota-atestare", methods=["POST", 'GET'])
async def nota_atestare(request):

    print(colored("request:", "blue"))
    print(request)
    print(colored("request json:", "blue"))
    print(request.json)
    print(colored("request args:", "blue"))
    print(request.args)
    print(request.method)
    print(colored("request args:", "blue"))
    print(request.args)

    print(colored("-------:", "blue"))

    if request.method=="POST":
        student = request.json.get("student", "")
        # student = request.args.get("student", "")
        # nota = request.args.get("nota", "")
        # nr_atestare = int(request.args.get("nr_atestare", ""))
        nota = request.json.get("nota", "")
        nr_atestare = int(request.json.get("nr_atestare", ""))

        is_uniq = await MidtermMark.is_unique(doc=dict(student=student, midterm_nr=nr_atestare))
        
        midterm_mark = await MidtermMark.find_one(filter={"midterm_nr":nr_atestare, "student":student})

        # if is_uniq in (True, None):
        if not midterm_mark:
            try:
                await MidtermMark.insert_one(dict(student=student, mark=int(nota), midterm_nr=nr_atestare, status="processing"))

                return response.json({"status": "success", "message": "Midterm mark saved successfully"})
            except:
                return response.json({"status": "error", "message": "Midterm mark not saved or student " + student + ". Error"})
        else:
            return response.json({"status": "error", "message": "This student already has mark for midterm " +str(nr_atestare) })        


    else: #GET
        """
        curl -X GET \
      -H "content-type: application/json" \
      -H "Accept: application/json" \
      -d '{"student":"Diana Marusic"}' \
      "http://127.0.0.1:8000/nota-examen"
      """

        student = request.args.get("student", "")        
        nr_atestare = int(request.args.get("nr_atestare", ""))

        # exam_mark = await ExamMark.find_one({"student":student}, as_raw=True)
        # midterm_mark = await MidtermMark.find_one({"student":student, "midterm_nr": nr_atestare})
        # midterm_mark = await MidtermMark.find_one({"student":student})
        midterm_mark = await MidtermMark.find_one(filter={"midterm_nr":nr_atestare, "student":student})
        print(colored("midterm mark:", "yellow"), midterm_mark)   

        if midterm_mark:
            return response.json({"status": "success", "student":student, "midterm mark": midterm_mark.mark, "midterm nr:": midterm_mark.midterm_nr})
        else:
            return response.json({
                "status": "success", 
                "student":student, 
                "midterm mark": None, 
                "midterm nr:": nr_atestare, 
                "message": "No marks found for student '" + student + "' for midterm " + str(nr_atestare)
            })


    return response.json({"status": "unknown", "message": "Something went wrong"})


@app.route("/nota-finala", methods=["GET"])
async def get_nota_finala(request):
    # student = request.args.get("student", "")
    print("request args:", request.args)
    print("request query args:", request.query_args)
    print("request query str:", request.query_string)
    
    student = request.args.get("student", "")

    print(colored("Student:" + str(student), "yellow"))
    # midterm_marks = await MidtermMark.find({"student":student})
    # midterm_marks = await MidtermMark.find({"student":student})

    try:
        # cursor_marks = await MidtermMark.find({"student":student})
        cursor_marks = await MidtermMark.find(sort='student')
        
        marks = cursor_marks.objects
        results = []
        for obj in marks:
            if obj.student == student:
                results.append(int(obj.mark))

        print("results marks:", results)
        # midterm_marks_cursor = await MidtermMark.find({"student":student})
        # # midterm_marks = await midterm_marks_cursor.to_list()

        # midterm_marks_cursor = midterm_marks_cursor.objects
        # midterm_marks = [] 

        # for obj in midterm_marks_cursor:
        #     midterm_marks.append(obj.mark)
        midterm_marks = results

        # TODO: finish
    except Exception as e:
        print(colored("ERROR!", "red"), e)
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
        final_mark = PERCENTAGE_EXAM / 100.0 * exam_mark + PERCENTAGE_M1/100.00 * midterm_marks[0] + PERCENTAGE_M2/100.00 * midterm_marks[1]

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
    

@app.route("/s2-validate-student-marks", methods=["POST"])
async def s2_validate_student_marks(request):
    print(colored("request:", "blue"))
    print(request)
    print(colored("request json:", "blue"))
    print(request.json)
    print(colored("-------:", "blue"))

    if request.method=="POST":
        print(colored("request args:", "green"))
        print(request.args)
        print(colored("request body:", "green"))
        print(request.body)
        print(colored("request form:", "green"))
        print(request.form)
        print(colored("-------:", "blue"))
        
        student = request.json.get("student", "")
        ttype = str(request.json.get("tip", "")) # poate fi "examen" sau "atestare"
        # student = request.form["student"]
        # ttype = str(request.form.get("tip", "")) # poate fi "examen" sau "atestare"
        if ttype=="examen":
            try:
                update = {"status": "finished"}
                await ExamMark.update_one({"student": student}, {"$set": update})

                return response.json({"status": "success", "message": "Exam mark validated successfully"})
            except:
                return response.json({"status": "error", "message": "Exam mark not validated for " + student + ". Error"})

        elif ttype=="atestare":
            try:
                update = {"status": "finished"}
                await MidtermMark.update_many({"student": student}, {"$set": update})

                return response.json({"status": "success", "message": "Midterm marks validated successfully"})
            except Exception as e:
                print(colored("Exception:", "red"), e)
                return response.json({"status": "error", "message": "Midterm marks not validated for " + student + ". Error"})
        else:
            return response.json({"status": "error", "message": "Parametrul 'tip' trebuie sa fie 'examen' sau 'atestare'!. Error"})


    return response.json({"status": "unknown", "message": "Something went wrong"})



@app.route("/status", methods=["GET"])
async def status(request):
    
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



########################################
# RPC
########################################

@jsonrpc
async def get_nota_examen(student):
    # exam_mark = await ExamMark.find_one({"student":student}, as_raw=True)
    exam_mark = await ExamMark.find_one({"student":student})
    print(colored("exam mark:", "yellow"), exam_mark)   

    print(colored("exam mark:", "yellow"), exam_mark.mark)   
    if exam_mark:
        return json.dumps({"status": "success", "student":student, "exam_mark": exam_mark.mark})
    else:
        return json.dumps({"status": "error", "message": "Exam mark not found for student " + student + ". Error"})
        
    return json.dumps({"status": "unknown", "message": "Something went wrong"})

@jsonrpc
async def post_nota_examen(student, nota):
    is_uniq = await ExamMark.is_unique(doc=dict(student=student))
    
    if is_uniq in (True, None):
        await ExamMark.insert_one(dict(student=student, mark=int(nota), status="processing"))

        return json.dumps({"status": "success", "message": "Exam mark saved successfully"})
    else:
        return json.dumps({"status": "error", "message": "This student already has exam mark!"})        

    
@jsonrpc
async def s2_get_nota_atestare(student, nr_atestare):
    nr_atestare = int(nr_atestare)
    # exam_mark = await ExamMark.find_one({"student":student}, as_raw=True)
    # midterm_mark = await MidtermMark.find_one({"student":student, "midterm_nr": nr_atestare})
    # midterm_mark = await MidtermMark.find_one({"student":student})
    midterm_mark = await MidtermMark.find_one(filter={"midterm_nr":nr_atestare, "student":student})
    print(colored("midterm mark:", "yellow"), midterm_mark)   

    if midterm_mark:
        return json.dumps({"status": "success", "student":student, "midterm mark": midterm_mark.mark, "midterm nr:": midterm_mark.midterm_nr})
    else:
        return json.dumps({
            "status": "success", 
            "student":student, 
            "midterm mark": None, 
            "midterm nr:": nr_atestare, 
            "message": "No marks found for student '" + student + "' for midterm " + str(nr_atestare)
        })


    return json.dumps({"status": "unknown", "message": "Something went wrong"})
    
@jsonrpc
async def s2_post_nota_atestare(student, nota, nr_atestare):
    try:
        nr_atestare = int(nr_atestare)
        nota = int(nota)
    except:
        return json.dumps({"status": "error", "message": "Wrong parameters " })        

    is_uniq = await MidtermMark.is_unique(doc=dict(student=student, midterm_nr=nr_atestare))
    
    midterm_mark = await MidtermMark.find_one(filter={"midterm_nr":nr_atestare, "student":student})

    # if is_uniq in (True, None):
    if not midterm_mark:
        try:
            await MidtermMark.insert_one(dict(student=student, mark=int(nota), midterm_nr=nr_atestare, status="processing"))

            return json.dumps({"status": "success", "message": "Midterm mark saved successfully"})
        except:
            return json.dumps({"status": "error", "message": "Midterm mark not saved or student " + student + ". Error"})
    else:
        return json.dumps({"status": "error", "message": "This student already has mark for midterm " +str(nr_atestare) })        

    
@jsonrpc
async def nota_finala(student):
    print(colored("Student:" + str(student), "yellow"))
    # midterm_marks = await MidtermMark.find({"student":student})
    # midterm_marks = await MidtermMark.find({"student":student})

    try:
        # cursor_marks = await MidtermMark.find({"student":student})
        cursor_marks = await MidtermMark.find(sort='student')
        
        marks = cursor_marks.objects
        print("marks", marks)
        results = []
        for obj in marks:
            if obj.student == student:
                results.append(int(obj.mark))

        print("results", results)
        # midterm_marks_cursor = await MidtermMark.find({"student":student})
        # # midterm_marks = await midterm_marks_cursor.to_list()

        # midterm_marks_cursor = midterm_marks_cursor.objects
        # midterm_marks = [] 

        # for obj in midterm_marks_cursor:
        #     midterm_marks.append(obj.mark)
        midterm_marks = results

        # TODO: finish
    except Exception as e:
        print(colored("ERROR!", "red"), e)
        print(colored("--Error!-- No midterm marks found for student " + student, "red"))
        return json.dumps({"status": "error", "message":"--Error!-- No midterm marks found for student " + student})

    # print(colored("---Midterm marks:", "blue"), midterm_marks)
    # exam_mark = await ExamMark.find_one({"student":student}).objects
    try:
        exam_mark = await ExamMark.find_one({"student":student})

        print(colored("---Exam mark:", "green"), exam_mark.mark)
        exam_mark = int(exam_mark.mark)
    except:
        print(colored("--Error!-- No exam mark found for student " + student))            
        return json.dumps({"status": "error", "message":"--Error!-- No exam mark found for student " + student})


    NR_MIDTERMS = 2
    PERCENTAGE_M1 = 30
    PERCENTAGE_M2 = 30
    PERCENTAGE_EXAM = 40
    
    if exam_mark and midterm_marks and (len(midterm_marks) == NR_MIDTERMS):
        final_mark = PERCENTAGE_EXAM / 100.0 * exam_mark + PERCENTAGE_M1/100.00 * midterm_marks[0] + PERCENTAGE_M2/100.00 * midterm_marks[1]

        return json.dumps({
            "status": "success", 
            "student":student,
            "note_atestari": midterm_marks, 
            "nota_examen": exam_mark, 
            "nota_finala": final_mark
        })

    elif len(midterm_marks) != NR_MIDTERMS:
        return json.dumps({
            "status":"error", 
            "message": "Nr of midterms for student " + student + " should be " + str(NR_MIDTERMS) + ", found " + str(len(midterm_marks) )
            }
        )
    else:
        return json.dumps({"status": "error", "message":"--Error!-- Something went wrong "})

    return json.dumps({"status": "unknown", "message": "Something went wrong"})
    
    
@jsonrpc
async def s2_validate_student_marks(student, tip):
    print("RPC!")
    ttype = tip
    if ttype == "examen":
        try:
            update = {"status": "finished"}
            await ExamMark.update_one({"student": student}, {"$set": update})

            return json.dumps({"status": "success", "message": "Exam mark validated successfully"})
        except:
            return json.dumps({"status": "error", "message": "Exam mark not validated for " + student + ". Error"})

    elif ttype=="atestare":
        try:
            update = {"status": "finished"}
            await MidtermMark.update_many({"student": student}, {"$set": update})

            return json.dumps({"status": "success", "message": "Midterm marks validated successfully"})
        except Exception as e:
            print(colored("Exception:", "red"), e)
            return json.dumps({"status": "error", "message": "Midterm marks not validated for " + student + ". Error"})
    else:
        return json.dumps({"status": "error", "message": "Parametrul 'tip' trebuie sa fie 'examen' sau 'atestare'!. Error"})

    return json.dumps({"status": "unknown", "message": "Something went wrong"})


@jsonrpc
async def status():
    try:
        nr_midterm_marks_processing = await MidtermMark.count_documents({'status': "processing"})
        nr_exam_marks_processing = await ExamMark.count_documents({'status': "processing"})
        return json.dumps({
            "status": "success", 
            "nr_midterm_marks_processing":nr_midterm_marks_processing, 
            "nr_exam_marks_processing": nr_exam_marks_processing, 
            "total_processing": nr_midterm_marks_processing + nr_exam_marks_processing
            })
    except:
        return json.dumps({"status": "error", "message": "Something went wrong"})

    return json.dumps({"status": "unknown", "message": "Something went wrong"})

@jsonrpc
async def get_all_exam_marks():
    try:    
        cursor_marks = await ExamMark.find(sort='student')
        marks = cursor_marks.objects
        
        results = {}
        for obj in marks:
            results[obj.student] = obj.mark

        return json.dumps({"status": "success", "results":results})
    except:
        return json.dumps({"status": "error", "message": "Something went wrong"})
    return json.dumps({"status": "unknown", "message": "Something went wrong"})

@jsonrpc
async def get_all_midterm_marks():
    try:    
        cursor_marks = await MidtermMark.find(sort='student')
        marks = cursor_marks.objects
        
        results = {}
        for obj in marks:
            results[obj.student] = {"midterm_nr": obj.midterm_nr, "mark": obj.mark}

        return json.dumps({"status": "success", "results":results})
    except:
        return json.dumps({"status": "error", "message": "Something went wrong"})
    return json.dumps({"status": "unknown", "message": "Something went wrong"})


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8000, debug=True)
    # 0.0.0.0 accesibil din retea
    
    app.run(host='0.0.0.0', port=8000, debug=True)