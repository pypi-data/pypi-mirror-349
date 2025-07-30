cmake_minimum_required(VERSION 3.15)
project(kws_decoder LANGUAGES CXX)

# Required for pybind11 to locate Python correctly
find_package(pybind11 REQUIRED)

# List your C++ sources
set(SOURCES
    ${CMAKE_CURRENT_SOURCE_DIR}/cpp/node.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/cpp/trie.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/cpp/counter.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/cpp/kws_decoder_core.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/cpp/kws_decoder.cpp
)

# Build the pybind11 module
pybind11_add_module(kws_decoder ${SOURCES})

# Optimization flags (optional, handled by most toolchains anyway)
target_compile_options(kws_decoder PRIVATE -O3 -Wall -fPIC)

# Optional: Name the output module explicitly
set_target_properties(kws_decoder PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/src/kws_decoder)
