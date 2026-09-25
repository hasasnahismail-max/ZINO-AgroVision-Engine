cmake_minimum_required(VERSION 3.15)
project(ZinoAgroVision)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED)

add_executable(zino_agro src/main.cpp)
target_link_libraries(zino_agro PRIVATE ${OpenCV_LIBS})
