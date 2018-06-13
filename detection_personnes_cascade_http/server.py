import json
import threading
import cv2
import sys
from bottle import run, post, request, response

casc_path = "haarcascade_frontalface_default.xml"

def vision_thread():
    global faces_num
    face_cascade = cv2.CascadeClassifier(casc_path)
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        _, frame = video_capture.read()

        # Resize frame so that the processing is faster
        height, width, _ =  frame.shape
        new_width = width / 2
        new_height = height / 2
        frame = cv2.resize(frame, (new_width, new_height))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        faces_num = len(faces)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.putText(frame, "%d faces detected" % faces_num,
            (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.CV_AA)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Exit on escape key
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

def server_thread():
    run(host='192.168.0.102', port=8080, debug=True)

@post('/faces')
def faces_req():
  req_obj = json.loads(request.body.read())
  return str(faces_num)

@post('/process')
def my_process():
  req_obj = json.loads(request.body.read())
  # do something with req_obj
  # ...
  return "OK"

faces_num = 0
t = threading.Thread(target=server_thread)
t.start()
vision_thread()
