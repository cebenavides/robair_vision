CC=g++
ARCH=-arch x86_64

SANDBOX_DIR=/usr/local/Cellar/opencv@2/2.4.13.6
INCLUDE_FLAGS=-I$(SANDBOX_DIR)/include

CFLAGS=-c -Wall $(INCLUDE_FLAGS)
LDFLAGS= -L$(SANDBOX_DIR)/lib -lopencv_calib3d -lopencv_core -lopencv_features2d -lopencv_flann -lopencv_highgui -lopencv_imgproc \
        -lopencv_ml -lopencv_objdetect -lopencv_photo -lopencv_stitching -lopencv_video -lopencv_videostab

SOURCES=camera_test.cpp
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=camera_test

all : $(SOURCES) $(EXECUTABLE)

clean :
	rm -f $(OBJECTS) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS) Makefile
	$(CC) $(ARCH) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@
