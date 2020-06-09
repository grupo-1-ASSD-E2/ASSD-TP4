cmake_minimum_required(VERSION 3.4.1)

add_library(ffi_google_oboe
            SHARED

            # Oboe ffi files
            src/main/cpp/ffiOboeExport.cpp
            src/main/cpp/OboeFfiStream.cpp

            # Audio engine files
            src/main/cpp/audio/AAssetDataSource.cpp

            # Utils files
#            src/main/cpp/utils/UtilityFunctions.cpp
        )


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

target_link_libraries(ffi_google_oboe oboe)