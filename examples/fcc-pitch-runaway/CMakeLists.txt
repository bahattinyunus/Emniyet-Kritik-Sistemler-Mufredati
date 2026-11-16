cmake_minimum_required(VERSION 3.10)
project(FCC_Pitch_Safety_Monitor C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Werror -pedantic")

include_directories(include)

# Kütüphane Hedefi
add_library(fcc_monitor src/fcc_pitch_monitor.c)

# Birim Test Hedefi
add_executable(test_fcc_monitor tests/test_fcc_pitch_monitor.c)
target_link_libraries(test_fcc_monitor fcc_monitor)

enable_testing()
add_test(NAME FccMonitorMcdcTests COMMAND test_fcc_monitor)
