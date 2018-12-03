cmake_minimum_required(VERSION 3.7)
project(rsacrt)

set(CMAKE_C_STANDARD 99)

set(CMAKE_C_FLAGS "-lgmp -O0")

set(SOURCE_FILES main.c city_rsa.c city_rsa.h)
add_executable(rsacrt ${SOURCE_FILES})
