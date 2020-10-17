from sanic_motor import BaseModel

# TODO: add necessary fields
class Student(BaseModel):
    __coll__ = 'students'
    __unique_fields__ = ['name']
    # __unique_fields__ = ['name, age']   # name and age for unique
