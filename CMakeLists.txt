cmake_minimum_required(VERSION 3.0)
project(webcam-detector)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -O2 -g")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -ldl -lrt")
message(STATUS "optional:-std=c++17")
set(OpenCV_DIR "/home/src/opencv-wayland/build/")
include_directories(/usr/include/freetype2/)
include_directories(/home/src/tensorflow/)
include_directories(/home/src/tensorflow/tensorflow/lite/tools/make/downloads/flatbuffers/include/)
find_package(OpenCV REQUIRED)
message(STATUS "OpenCV library status:")
message(STATUS " version: ${OpenCV_VERSION}")
message(STATUS " libraries: ${OpenCV_LIBS}")
message(STATUS " include path: ${OpenCV_INCLUDE_DIRS}")
include_directories( ${OpenCV_INCLUDE_DIRS} )
ADD_LIBRARY(TFlite_LIB STATIC IMPORTED)
SET_TARGET_PROPERTIES(TFlite_LIB PROPERTIES
IMPORTED_LOCATION /home/src/webcam-detect-tflite/libs/libtensorflow-lite.a)
set(SOURCE_FILES
main.cxx)
add_executable(${PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS} )
target_link_libraries(${PROJECT_NAME}
freetype
pthread
dl
)
target_link_libraries(${PROJECT_NAME} TFlite_LIB)
