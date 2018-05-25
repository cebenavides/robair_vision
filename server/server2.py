import json

from bottle import run, post, request, response

@post('/process')
def my_process():
  req_obj = json.loads(request.body.read())
  # do something with req_obj
  # ...
  return 'EL VIEJO BARBUDON'

run(host='192.168.0.102', port=8080, debug=True)
