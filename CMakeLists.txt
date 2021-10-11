cmake_minimum_required(VERSION 3.19)
project(flutter_engine_build LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)

file(GLOB_RECURSE SOURCES LIST_DIRECTORIES false RELATIVE "${CMAKE_CURRENT_LIST_DIR}"
        "${CMAKE_CURRENT_LIST_DIR}/engine/src/flutter/*.cc"
        "${CMAKE_CURRENT_LIST_DIR}/engine/src/flutter/*.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/engine/src/flutter/*.h"
        "${CMAKE_SOURCE_DIR}/engine/src/flutter/*.gn")
find_package(ICU REQUIRED COMPONENTS uc dt in io)
find_package(harfbuzz CONFIG REQUIRED)

add_subdirectory("${CMAKE_SOURCE_DIR}/engine/src/third_party/googletest")
#add_subdirectory("${CMAKE_SOURCE_DIR}/engine/src/third_party/benchmark")

add_executable(engine_build ${SOURCES})
target_link_libraries(engine_build PRIVATE GTest::gmock GTest::gtest  ICU::uc harfbuzz)
target_include_directories(engine_build PRIVATE
        "${CMAKE_SOURCE_DIR}/engine/src"
        "${CMAKE_SOURCE_DIR}/engine/src/flutter"
        "${CMAKE_SOURCE_DIR}/engine/src/flutter/third_party"
        "${CMAKE_SOURCE_DIR}/engine/src/third_party/benchmark"
        "${CMAKE_SOURCE_DIR}/engine/src/third_party/skia"
        "${CMAKE_SOURCE_DIR}/engine/src/third_party/txt/src")
