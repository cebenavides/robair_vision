import cv2
import sys

casc_path = "haarcascade_frontalface_default.xml"

def main():
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

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.putText(frame, "%d faces detected" % len(faces),
            (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.CV_AA)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Exit on escape key
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
