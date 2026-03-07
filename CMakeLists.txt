cmake_minimum_required(VERSION 3.15)
project(LaserElectronSimulation LANGUAGES C)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED True)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin)

find_package(OpenMP REQUIRED)
find_library(MATH_LIBRARY m REQUIRED)

option(GENERIC "Build for generic x86 architecture instead of native" OFF)
if(GENERIC)
    add_compile_options(-mtune=generic)
else()
    add_compile_options(-march=native)
endif()

add_compile_options(-s -O3)

file(MAKE_DIRECTORY 
    ${CMAKE_CURRENT_SOURCE_DIR}/output 
    ${CMAKE_CURRENT_SOURCE_DIR}/output-image 
    ${CMAKE_CURRENT_SOURCE_DIR}/output-video 
    ${CMAKE_CURRENT_SOURCE_DIR}/input
)

add_library(physics_modules OBJECT
    src/particle_push.c
    src/tools.c
    src/init.c
    src/ponderomotive.c
    src/potentials.c
)

target_include_directories(physics_modules PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(physics_modules PUBLIC OpenMP::OpenMP_C)

add_executable(laser_electron src/laser_electron.c)
target_link_libraries(laser_electron PRIVATE physics_modules OpenMP::OpenMP_C ${MATH_LIBRARY})

add_executable(analytic_solution src/analytic_solution.c)
target_link_libraries(analytic_solution PRIVATE physics_modules OpenMP::OpenMP_C ${MATH_LIBRARY})

set(UTILITY_SRCS 
    error_calc 
    find_enter_exit_time 
    find_final_p 
    find_max_p
)

foreach(util_name IN LISTS UTILITY_SRCS)
    add_executable(${util_name} src/${util_name}.c)
    target_include_directories(${util_name} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
    target_link_libraries(${util_name} PRIVATE OpenMP::OpenMP_C ${MATH_LIBRARY})
endforeach()

add_custom_target(clean-output
    COMMAND ${CMAKE_COMMAND} -E rm -rf
        ${CMAKE_CURRENT_SOURCE_DIR}/output
        ${CMAKE_CURRENT_SOURCE_DIR}/output-image
        ${CMAKE_CURRENT_SOURCE_DIR}/output-video
        ${CMAKE_CURRENT_SOURCE_DIR}/input
    COMMENT "Removed output directories."
)