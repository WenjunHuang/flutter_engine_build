cmake_minimum_required(VERSION 3.19)
project(flutter_engine_build LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)

file(GLOB_RECURSE SOURCES RELATIVE "${CMAKE_SOURCE_DIR}" "${CMAKE_SOURCE_DIR}/engine/src/flutter/*.cc" "${CMAKE_SOURCE_DIR}/engine/src/flutter/*.h" "${CMAKE_SOURCE_DIR}/engine/src/flutter/*.gn")

add_subdirectory("${CMAKE_SOURCE_DIR}/engine/src/third_party/googletest")
add_subdirectory("${CMAKE_SOURCE_DIR}/engine/src/third_party/benchmark")

add_library(engine_build "${SOURCES}")
target_link_libraries(engine_build PRIVATE GTest::gmock GTest::gtest benchmark)
target_include_directories(engine_build PRIVATE
        "${CMAKE_SOURCE_DIR}/engine/src"
        "${CMAKE_SOURCE_DIR}/engine/src/flutter"
        "${CMAKE_SOURCE_DIR}/engine/src/flutter/third_party")