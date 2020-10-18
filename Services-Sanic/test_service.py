
import requests
import json
from termcolor import colored
import pprint


TEST_WITH_GATEWAY = True
# TEST_WITH_GATEWAY = False
SERVICE_ADDRESS = 'http://127.0.0.1:8000'

if TEST_WITH_GATEWAY==True:
    # going through gateway
    SERVICE_ADDRESS = 'http://127.0.0.1:5000'


pp = pprint.PrettyPrinter(indent=4)

def make_request(method, endpoint, parameters):
    if method=='GET':
        r = requests.get(endpoint, params=parameters)
    elif method=='POST':
        #r = requests.post(endpoint, data=json.dumps(parameters))
        r = requests.post(endpoint, data=json.dumps(parameters))
    elif method=='PUT':
        r = requests.put(endpoint, data=parameters)
    elif method=='DELETE':
        r = requests.delete(endpoint)


def post_exam_mark():
    endpoint = SERVICE_ADDRESS + "/nota-examen"

    print(colored("-------REQUEST " + endpoint, "blue"))

    parameters = {
        "student": "Student Test3",
        "nota": 9
    }    

    print("parameters:",parameters)

    try:
        #r = requests.post(endpoint, data=json.dumps(parameters))
        r = requests.post(endpoint, data=json.dumps(parameters))
        # r = requests.post(endpoint, json=parameters)
        print(colored("response:---", "green"))
        print(colored("status code:"+str(r.status_code), "yellow"))
        pp.pprint(r.json())
    except Exception as e:
        print(colored("---error in request", "red"), e)
        # print(colored(str(r), "red"))
        # print(colored(str(r.text), "red"))



def get_all_exam_marks():
    endpoint = SERVICE_ADDRESS + "/get-all-exam-marks"

    print(colored("-------REQUEST " + endpoint, "blue"))

    try:
        # #r = requests.post(endpoint, data=json.dumps(parameters))
        # r = requests.post(endpoint, data=json.dumps(parameters))
        r = requests.get(endpoint)
        print(colored("response:---", "green"))
        print(colored("status code:"+str(r.status_code), "yellow"))
        pp.pprint(r.json())
    except Exception as e:
        print(colored("---error in request", "red"), e)
        # print(colored(str(r), "red"))
        # print(colored(str(r.text), "red"))


def get_exam_mark():
    endpoint = SERVICE_ADDRESS + "/nota-examen"

    print(colored("-------REQUEST " + endpoint, "blue"))

    parameters = {
        "student": "Student Test3",
    }    

    print("parameters:",parameters)

    try:
        # #r = requests.post(endpoint, data=json.dumps(parameters))
        r = requests.post(endpoint, data=json.dumps(parameters))
        # r = requests.get(endpoint, json=parameters)
        # r = requests.get(endpoint, params=parameters)
        print(colored("response:---", "green"))
        print(colored("status code:"+str(r.status_code), "yellow"))
        pp.pprint(r.json())
    except Exception as e:
        print(colored("---error in request", "red"), e)
        # print(colored(str(r), "red"))
        # print(colored(str(r.text), "red"))

def test_get_midterm_mark(existing=True):
    endpoint = SERVICE_ADDRESS + "/s2-nota-atestare"

    print(colored("-------REQUEST " + endpoint, "blue"))

    parameters = {
        "student": "Student Test3",
        "nr_atestare": 1
    }   
     #if want to test not found mark 
    if existing == False:
        parameters["nr_atestare"] = -2



    print("parameters:",parameters)

    try:
        # r = requests.get(endpoint, json=parameters)
        r = requests.get(endpoint, params=parameters)
        print(colored("response:---", "green"))
        print(colored("status code:"+str(r.status_code), "yellow"))
        pp.pprint(r.json())
    except Exception as e:
        print(colored("---error in request", "red"), e)
        # print(colored(str(r), "red"))
        # print(colored(str(r.text), "red"))

def test_post_midterm_mark(midterm_nr=1):
    endpoint = SERVICE_ADDRESS + "/s2-nota-atestare"

    print(colored("-------REQUEST " + endpoint, "blue"))

    parameters = {
        "student": "Student Test3",
        "nota" : 7,
        "nr_atestare":midterm_nr
    }    

    print("parameters:",parameters)

    try:
        r = requests.post(endpoint, data=json.dumps(parameters))
        # r = requests.post(endpoint, data=json.dumps(parameters))
        # r = requests.post(endpoint, json=parameters)
        print(colored("response:---", "green"))
        print(colored("status code:"+str(r.status_code), "yellow"))
        pp.pprint(r.json())
    except Exception as e:
        print(colored("---error in request", "red"), e)
        # print(colored(str(r), "red"))
        # print(colored(str(r.text), "red"))


def get_all_midterm_marks():
    endpoint = SERVICE_ADDRESS + "/get-all-midterm-marks"

    print(colored("-------REQUEST " + endpoint, "blue"))

    try:
        # #r = requests.post(endpoint, data=json.dumps(parameters))
        # r = requests.post(endpoint, data=json.dumps(parameters))
        r = requests.get(endpoint)
        print(colored("response:---", "green"))
        print(colored("status code:"+str(r.status_code), "yellow"))
        pp.pprint(r.json())
    except Exception as e:
        print(colored("---error in request", "red"), e)
        # print(colored(str(r), "red"))
        # print(colored(str(r.text), "red"))


def get_final_mark():
    endpoint = SERVICE_ADDRESS + "/nota-finala"

    print(colored("-------REQUEST " + endpoint, "blue"))

    parameters = {
        "student": "Student Test3",
    }   

    print("parameters:",parameters)

    try:
        # r = requests.get(endpoint, json=parameters)
        r = requests.get(endpoint, params=parameters)
        print(colored("response:---", "green"))
        print(colored("status code:"+str(r.status_code), "yellow"))
        pp.pprint(r.json())
    except Exception as e:
        print(colored("---error in request", "red"), e)
        # print(colored(str(r), "red"))
        # print(colored(str(r.text), "red"))


def get_status():
    endpoint = SERVICE_ADDRESS + "/status"
    if TEST_WITH_GATEWAY==True:
        endpoint = SERVICE_ADDRESS + "/s2-status"


    print(colored("-------REQUEST " + endpoint, "blue"))

    try:
        r = requests.get(endpoint)
        print(colored("response:---", "green"))
        print(colored("status code:"+str(r.status_code), "yellow"))
        pp.pprint(r.json())
    except Exception as e:
        print(colored("---error in request", "red"), e)
        # print(colored(str(r), "red"))
        # print(colored(str(r.text), "red"))


def test_validate_marks(ttype):
    """type should be 'atestare' or 'examen'"""
    endpoint = SERVICE_ADDRESS + "/s2-validate-student-marks"

    print(colored("-------REQUEST " + endpoint, "blue"))

    parameters = {
        "student": "Student Test3",
        "tip": ttype
    }   

    print("parameters:",parameters)

    try:
        # r = requests.post(endpoint, json=parameters)
        r = requests.post(endpoint, data=json.dumps(parameters))
        # r = requests.post(endpoint, data=json.dumps(parameters))

        print(colored("response:---", "green"))
        print(colored("status code:"+str(r.status_code), "yellow"))
        pp.pprint(r.json())
    except Exception as e:
        print(colored("---error in request", "red"), e)
        # print(colored(str(r), "red"))
        # print(colored(str(r.text), "red"))

def test_validate_exam_marks():
    test_validate_marks(ttype="examen")

def test_validate_midterm_marks():
    test_validate_marks(ttype="atestare")

if __name__ == '__main__':
    post_exam_mark()
    get_all_exam_marks()
    get_exam_mark()
    # print("-----------")
    test_post_midterm_mark(midterm_nr=1)
    test_post_midterm_mark(midterm_nr=2)
    # test_post_midterm_mark(midterm_nr=3)

    get_all_midterm_marks()
    # print("-----------")
    test_get_midterm_mark()

    test_get_midterm_mark(existing=False) #shoudl return "no marks found"

    # print("-----------")
    get_final_mark()  
    
    get_status()

    test_validate_exam_marks()
    # test_validate_midterm_marks()

    get_status()
    # 
