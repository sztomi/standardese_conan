project(mytest)
cmake_minimum_required(VERSION 3.4.2)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(test_package main.cpp)

set (CMAKE_CXX_STANDARD 11)

target_link_libraries(test_package ${CONAN_LIBS})
