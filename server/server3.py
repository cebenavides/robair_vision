import json
import threading
from bottle import run, post, request, response

def counter_func():
    global counter
    while(1):
        counter = counter + 1

def server_func():
    run(host='192.168.0.102', port=8080, debug=True)

@post('/process')
def my_process():
  req_obj = json.loads(request.body.read())
  # do something with req_obj
  # ...
  return str(counter)

counter = 0
t1 = threading.Thread(target=counter_func)
t1.start()
t2 = threading.Thread(target=server_func)
t2.start()
