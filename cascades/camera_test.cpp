#include "opencv2/opencv.hpp"
#include <iostream>

using namespace std;

void detectAndDisplay(cv::Mat frame);

const string CASCADE_PATH = "/usr/local/Cellar/opencv@2/2.4.13.6/share/OpenCV/haarcascades/haarcascade_mcs_upperbody.xml";
cv::CascadeClassifier face_cascade;
cv::VideoWriter video;
int frame_width, frame_height;

int main(int argc, const char** argv){
  cv::VideoCapture cap(0);

  if (!cap.isOpened()) {
    cout << "Error opening camera" << endl;
    return -1;
  }

  if (!face_cascade.load(CASCADE_PATH)) {
    cout << "Error loading face cascade" << endl;
    return -1;
  }

  frame_width = cap.get(CV_CAP_PROP_FRAME_WIDTH) / 2;
  frame_height = cap.get(CV_CAP_PROP_FRAME_HEIGHT) / 2;

  video = cv::VideoWriter("outcpp.avi", CV_FOURCC('M','J','P','G'), 10, cv::Size(frame_width,frame_height));

  while(1) {
    cv::Mat frame;
    cap >> frame;

    if (frame.empty())
      break;

    detectAndDisplay(frame);

    char c = (char)cv::waitKey(1);
    if( c == 27 )
      break;
  }

  cap.release();
  video.release();
  cv::destroyAllWindows();

  return 0;
}

void detectAndDisplay(cv::Mat frame){
  cv::resize(frame, frame, cv::Size(frame_width, frame_height));

  std::vector<cv::Rect> faces;
  cv::Mat frame_gray;

  cv::cvtColor(frame, frame_gray, CV_BGR2GRAY);
  cv::equalizeHist(frame_gray, frame_gray);

  face_cascade.detectMultiScale(frame_gray, faces, 1.1, 5, 0|CV_HAAR_SCALE_IMAGE, cv::Size(30, 30));
  for (size_t i = 0; i < faces.size(); i++) {
    cv::rectangle(frame, faces[i], cv::Scalar( 0, 255, 0), 2);
  }

  video.write(frame);
  cv::imshow("Camera", frame);
}
