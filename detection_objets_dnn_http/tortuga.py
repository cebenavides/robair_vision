import turtle
import http.client

c = http.client.HTTPConnection('localhost', 8080)

def tortuga():
    turtle.shape("turtle")
    turtle.speed("slowest")
    while True:
        c.request('POST', '/process', '{}')
        doc = c.getresponse().read()
        print(doc)
        if doc == "1":
            turtle.forward(50)

tortuga()
