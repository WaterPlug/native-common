cmake_minimum_required(VERSION 3.28)
set(PROJECT_NAME wp_common)
project(${PROJECT_NAME})

set(CMAKE_CXX_STANDARD 20)

set(SOURCE_FILES
        base64.cpp
)

add_library(${PROJECT_NAME} STATIC ${SOURCE_FILES})

find_package(boost REQUIRED)

target_include_directories(${PROJECT_NAME} PUBLIC include)
target_link_libraries(${PROJECT_NAME} boost::boost)
if (NOT MSVC)
#    target_compile_options(${PROJECT_NAME} PUBLIC -Wno-format-nonliteral) # for fmt's chrono build
    target_compile_options(${PROJECT_NAME} PRIVATE -fno-exceptions)
else ()
    target_compile_definitions(${PROJECT_NAME} PRIVATE
            WIN32_LEAN_AND_MEAN
            NOMINMAX)
    target_link_libraries(${PROJECT_NAME} wsock32 ws2_32)
endif ()
target_compile_definitions(${PROJECT_NAME} PUBLIC FMT_EXCEPTIONS=0)

#enable_testing()
#include(../cmake/add_unit_test.cmake)
link_libraries(${PROJECT_NAME})
#set(TEST_DIR ${CMAKE_CURRENT_SOURCE_DIR}/test)
