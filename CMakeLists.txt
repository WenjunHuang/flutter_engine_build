cmake_minimum_required(VERSION 3.19)
project(flutter_engine_build LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)

file(GLOB_RECURSE SOURCES RELATIVE "${CMAKE_SOURCE_DIR}" "${CMAKE_SOURCE_DIR}/engine/src/flutter/*.cc" "${CMAKE_SOURCE_DIR}/engine/src/flutter/*.h" "${CMAKE_SOURCE_DIR}/engine/src/flutter/*.gn")

#file(GLOB_RECURSE FML_SRCS "flutter/fml/*.cc")
#list(FILTER FML_SRCS EXCLUDE REGEX "[\\w]*_unittest[s]?.cc")
#list(FILTER FML_SRCS EXCLUDE REGEX "backtrace.cc")
#add_library(FML_LIB "${FML_SRCS}")
##message("${FML_SRCS}")
#target_include_directories(FML_LIB PUBLIC "${CMAKE_SOURCE_DIR}")
#
#add_executable(fml_1 experiments/fml/main.cc)
#target_link_libraries(fml_1 PRIVATE FML_LIB)

add_subdirectory("${CMAKE_SOURCE_DIR}/engine/src/third_party/googletest")

add_library(engine_build "${SOURCES}")
target_link_libraries(engine_build PRIVATE GTest::gmock GTest::gtest)
target_include_directories(engine_build PRIVATE "${CMAKE_SOURCE_DIR}/engine/src" "${CMAKE_SOURCE_DIR}/engine/src/flutter"
        "${CMAKE_SOURCE_DIR}/engine/src/flutter/third_party")