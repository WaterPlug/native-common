cmake_minimum_required(VERSION 3.28)
if(NOT CMAKE_INSTALL_PREFIX MATCHES "conan2")
    set(CMAKE_PROJECT_TOP_LEVEL_INCLUDES "cmake/conan_provider.cmake")
endif()


project(native_common CXX)
set(unit_name ${native_common})
set(CMAKE_CXX_STANDARD 20 )


set(CMAKE_MSVC_RUNTIME_LIBRARY MultiThreaded)

# Better stack traces in Sentry
if (MSVC)
    add_compile_options(/Oy-)
    set(CMAKE_CXX20_STANDARD_COMPILE_OPTION ${CMAKE_CXX20_STANDARD_COMPILE_OPTION} -Zc:char8_t- /MT)
    set(CMAKE_CXX20_EXTENSION_COMPILE_OPTION ${CMAKE_CXX20_EXTENSION_COMPILE_OPTION} -Zc:char8_t- /MT)
else ()
    add_compile_options(-fno-omit-frame-pointer)
endif ()

if(SANITIZE)
    add_compile_options("-fsanitize=address")
    link_libraries("-fsanitize=address")
endif(SANITIZE)

add_subdirectory(common)
#enable_testing()

find_package(Python3 COMPONENTS Interpreter REQUIRED)
add_custom_target(
        conan_export_local
        COMMAND ${Python3_EXECUTABLE} ${CMAKE_SOURCE_DIR}/scripts/conan_local_export.py
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        COMMENT "Exporting local Conan package"
)