
import requests
import json
from termcolor import colored
import pprint

SERVICE_ADDRESS = 'http://127.0.0.1:8000'
pp = pprint.PrettyPrinter(indent=4)

def make_request(method, endpoint, parameters):
    if method=='GET':
        r = requests.get(endpoint, params=parameters)
    elif method=='POST':
        r = requests.post(endpoint, data=parameters)
    elif method=='PUT':
        r = requests.put(endpoint, data=parameters)
    elif method=='DELETE':
        r = requests.delete(endpoint)


def post_exam_mark():
    endpoint = SERVICE_ADDRESS + "/nota-examen"

    print(colored("-------REQUEST " + endpoint, "blue"))

    parameters = {
        "student": "Lorem Ipsum",
        "nota": 9
    }    

    print("parameters:",parameters)

    try:
        # r = requests.post(endpoint, data=parameters)
        r = requests.post(endpoint, json=parameters)
        print(colored("response:---", "green"))
        print(colored("status code:"+str(r.status_code), "red"))
        pp.pprint(r.json())
    except Exception as e:
        print(colored("---error in request", "red"), e)
        # print(colored(str(r), "red"))
        # print(colored(str(r.text), "red"))



def get_all_exam_marks():
    endpoint = SERVICE_ADDRESS + "/get-all-exam-marks"

    print(colored("-------REQUEST " + endpoint, "blue"))

    try:
        # r = requests.post(endpoint, data=parameters)
        r = requests.get(endpoint)
        print(colored("response:---", "green"))
        print(colored("status code:"+str(r.status_code), "red"))
        pp.pprint(r.json())
    except Exception as e:
        print(colored("---error in request", "red"), e)
        # print(colored(str(r), "red"))
        # print(colored(str(r.text), "red"))


if __name__ == '__main__':
    # post_exam_mark()
    get_all_exam_marks()