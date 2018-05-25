import httplib

c = httplib.HTTPConnection('localhost', 8080)
c.request('POST', '/process', '{}')
doc = c.getresponse().read()
print doc
