from sanic_motor import BaseModel

# TODO: add necessary fields
# class Student(BaseModel):
#     __coll__ = 'students'
#     __unique_fields__ = ['name']
#     # __unique_fields__ = ['name, age']   # name and age for unique


# {
# 	"id" : "1",
# 	"student": "NumePrenume",
# 	"mark": 10,
# 	"status": "processing"
# },
# nu stiu daca trebuie id
class ExamMark(BaseModel):
    __coll__ = 'exam_marks'
    # __unique_fields__ = ['name']


class MidtermMark(BaseModel):
    __coll__ = 'midterm_marks'



	