cmake_minimum_required(VERSION 3.4.2)

# Require C++17 compiler with no extensions
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(ffi_google_oboe
        SHARED

        # Oboe ffi files
        src/main/cpp/ffiOboeExport.cpp
        src/main/cpp/OboeFfiStream.cpp
        src/main/cpp/DSPCallback.cpp

        # Audio engine files
        src/main/cpp/audio/AAssetDataSource.cpp
        src/main/cpp/audio/Player.cpp

        # Utils files
        #            src/main/cpp/utils/UtilityFunctions.cpp
        )

# Compile with warnings for safety
if(MSVC)
    target_compile_options(ffi_google_oboe PRIVATE /W4 /WX)
else()
    target_compile_options(ffi_google_oboe PRIVATE -Wall -Wextra -pedantic)
endif()


# Set the path to the Oboe directory.
set (OBOE_DIR ../../oboe)

# Add the Oboe library as a subdirectory in your project.
# add_subdirectory tells CMake to look in this directory to
# compile oboe source files using oboe's CMake file.
# ./oboe specifies where the compiled binaries will be stored
add_subdirectory (${OBOE_DIR} ./oboe)

# Specify the path to the Oboe header files.
# This allows targets compiled with this CMake (application code)
# to see public Oboe headers, in order to access its API.
include_directories (
        ${OBOE_DIR}/include
        src/main/cpp
)

target_link_libraries(
        ffi_google_oboe
        oboe

        # Links the log library to the target library.
        ${log-lib}
)