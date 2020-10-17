from models import ExamMark, MidtermMark
from sanic import response

class MarksController:
    # def init_student(student):
    #   if student:
 #            is_uniq = await Student.is_unique(doc=dict(name=name))
 #            if is_uniq in (True, None):
 #              await Student.insert_one(dict(name=name, mark=int(mark)))
        
 #                return response.json({"status": "success", "message": "Student user created successfully"})
 #                # return redirect(app.url_for("index"))
 #            else:
 #                # request["flash"]("This name was already taken", "error")
 #                return response.json({"status":"error", "message": "This student with this name already exists"})

 #        # request["flash"]("User name is required", "error")
 #        return response.json({"status":"error", "message": "Student name is required (student parameter)"})

 #    # asta era pentru get cu formular in frontend
 #    # return jinja.render("form.html", request, user={})
 #    return response.json({"status": "success", "message": "Student user created successfully"})


    async def save_exam_mark(self, student, mark):
        await ExamMark.insert_one(dict(student=student, mark=int(mark), status="processing"))

        return response.json({"status": "success", "message": "Exam mark saved successfully"})
    
    # added to change mark status
    async def validate_exam_mark(self, student, mark):
        exam_mark = await ExamMark.find_one(id)
        try:
            await ExamMark.update_one({"_id": exam_mark.id}, {"$set": dict(status="finished")})
            return response.json({"status": "success", "message": "Exam mark validated successfully"})
        except:
            return response.json({"status": "error", "message": "Exam mark not validated. Error"})
        

    async def get_exam_mark(self, student):
        exam_mark = await ExamMark.find_one({"student":student})
        if exam_mark:
            return response.json({"status": "success", "exam_mark": int(exam_mark)})
        return response.json({"status": "error", "message": "Exam mark not found for student " + student + ". Error"})
        

        # TODO

    async def save_midterm_mark(self, student, mark, midterm_nr):
        pass
        # TODO

    async def get_final_mark(self, student):
        pass
        # TODO

    async def get_stats(self, student):
        pass
        # TODO

    # nu cred ca trebuie
    # async def get_all_students(self):
    #     st = await Student.find(sort='name')
    #     return st.objects
    # 