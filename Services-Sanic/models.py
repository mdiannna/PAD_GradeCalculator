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
    __unique_fields__ = ['student']


# {
# 	"id" : "1",
# 	"student": "NumePrenume",
# 	"mark": 10,
# 	"midterm_nr" : 1,
# 	"status": "processing"
# },

class MidtermMark(BaseModel):
    __coll__ = 'midterm_marks'



	