cmake_minimum_required(VERSION 3.10)
project(RTA_Simplex_Drone_Monitor C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Emniyet-Kritik Derleyici Uyarı Bayrakları (MISRA & Determinizm Denetimi)
add_compile_options(-Wall -Wextra -Werror -Wpedantic -Wconversion -Wshadow)

include_directories(include)

add_executable(test_rta_simplex
    src/rta_simplex_monitor.c
    tests/test_rta_simplex_monitor.c
)
