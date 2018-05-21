cmake_minimum_required(VERSION 3.8)

project(calc_flow)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

find_package(OpenCV REQUIRED)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME} PUBLIC opencv_core PRIVATE ${OpenCV_LIBS})