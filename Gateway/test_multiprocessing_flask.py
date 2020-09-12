from multiprocessing import Pool
from flask import Flask
# from flask import jsonify
# import ast
# import pandas as pd
# import requests
 
app = Flask(__name__)
_pool = None

a = 1


def test_hello(name):
	print("Hello world!", name)
	return "Hello "+ name


@app.route('/')
def index():
	return "try to access /hello-multi"


@app.route('/hello-multi')
def hello_multiprocess():
	"""returns pandas dataframe into HTML for health-check Services"""
	# resp_pool = _pool.map(get_response,tasks)
	global a

	resp_pool = _pool.map(test_hello, str(a))
	a+=1
	
	# table_frame= pd.DataFrame([ast.literal_eval(resp) for resp in resp_pool])
	# return table_frame.to_html()
	print("response:", resp_pool)

	return str(resp_pool)
 
if __name__=='__main__':
	# __main__pool = Pool(processes=12) # this is important part- We
	_pool = Pool(processes=12) # this is important part- We
	try:
		# insert production server deployment code
		# app.run(use_reloader=True)
		app.run()
	except KeyboardInterrupt:
		_pool.close()
		_pool.join()
	 