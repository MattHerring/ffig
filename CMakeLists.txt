cmake_minimum_required(VERSION 2.8)

# FIXME: This silences a warning but I'm not sure why its needed.
set(CMAKE_MACOSX_RPATH 1)

project(test_ffig)

set(CMAKE_CXX_FLAGS "-std=c++14")

include_directories(externals/catch/include)
include_directories(externals/variant/include)

find_package(PythonInterp REQUIRED)
find_package(Ruby REQUIRED)

function(add_ffig_library module input)
  add_custom_command(OUTPUT ${CMAKE_BINARY_DIR}/generated/${module}_c.h ${CMAKE_BINARY_DIR}/generated/${module}_c.cpp
    COMMAND ${PYTHON_EXECUTABLE} FFIG.py -i ${input} -m ${module} -t ${CMAKE_SOURCE_DIR}/templates -b _cpp.h.tmpl _mocks.h.tmpl rb.tmpl py.tmpl _c.h.tmpl _c.cpp.tmpl -o ${CMAKE_BINARY_DIR}/generated
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})

  # FIXME: This is a bit ugly. The header is copied next to the generated bindings.
  file(COPY ${input} DESTINATION ${CMAKE_BINARY_DIR}/generated/)

  add_library(${module}_c SHARED ${input} ${CMAKE_BINARY_DIR}/generated/${module}_c.h ${CMAKE_BINARY_DIR}/generated/${module}_c.cpp)

  # FIXME: This is a bit ugly. The shared library is copied next to the generated bindings.
  add_custom_command(TARGET ${module}_c
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${module}_c> ${CMAKE_BINARY_DIR}/generated/)
endfunction()

add_ffig_library(Shape input/Shape.h)
add_ffig_library(Tree input/Tree.h)
add_ffig_library(Asset input/Asset.h)

add_subdirectory(tests/src)

enable_testing()

add_test(
  NAME test_cppmodel
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_SOURCE_DIR}/tests/cppmodel
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})

add_test(
  NAME test_python_bindings
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_SOURCE_DIR}/tests
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)

add_test(
  NAME test_ruby_bindings
  COMMAND ${RUBY_EXECUTABLE} ${CMAKE_SOURCE_DIR}/tests/TestShape.rb ${CMAKE_SOURCE_DIR}/tests/TestShape.rb
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)

add_test(
  NAME test_cpp_mocks
  COMMAND ${CMAKE_BINARY_DIR}/tests/src/TestShapeMocks
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)

add_test(
  NAME test_cpp_circle
  COMMAND ${CMAKE_BINARY_DIR}/tests/src/TestCppCircle
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)

add_test(
  NAME test_cpp_tree
  COMMAND ${CMAKE_BINARY_DIR}/tests/src/TestCppTree
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)

