cmake_minimum_required(VERSION 3.4.2)

# Require C++17 compiler with no extensions
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

#file(GLOB_RECURSE SOURCES RELATIVE ${CMAKE_SOURCE_DIR} "src/main/cpp/SDL/src/thread/*.c")
file(GLOB SDL_SOURCES_1 RELATIVE ${CMAKE_SOURCE_DIR} "src/main/cpp/SDL/src/*.c")
file(GLOB SDL_SOURCES_2 RELATIVE ${CMAKE_SOURCE_DIR} "src/main/cpp/SDL/src/core/android/*.c")
file(GLOB SDL_SOURCES_3 RELATIVE ${CMAKE_SOURCE_DIR} "src/main/cpp/SDL/src/dynapi/*.c")
file(GLOB SDL_SOURCES_4 RELATIVE ${CMAKE_SOURCE_DIR} "src/main/cpp/SDL/src/atomic/*.c")
file(GLOB_RECURSE SDL_SOURCES_6 RELATIVE ${CMAKE_SOURCE_DIR} "src/main/cpp/SDL/src/video/*.c")

add_library(ffi_google_oboe
        SHARED

        # Oboe ffi files
        src/main/cpp/ffiOboeExport.cpp
        src/main/cpp/OboeFfiStream.cpp
        src/main/cpp/DSPCallback.cpp

        # Audio engine files
        src/main/cpp/audio/AAssetDataSource.cpp
        src/main/cpp/audio/Player.cpp

        # SDL source files
        ${SDL_SOURCES_1}
        ${SDL_SOURCES_2}
        ${SDL_SOURCES_3}
        ${SDL_SOURCES_4}
        ${SDL_SOURCES_5}
        ${SDL_SOURCES_6}

        # Utils files
        #            src/main/cpp/utils/UtilityFunctions.cpp
        )


set (TARGET_LIBS log android oboe GLESv2)
target_sources( ffi_google_oboe PRIVATE src/main/cpp/audio/NDKExtractor.cpp )
set (TARGET_LIBS ${TARGET_LIBS} mediandk)
target_link_libraries( ffi_google_oboe ${TARGET_LIBS} )

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
        src/main/cpp/SDL/include
)

target_link_libraries(
        ffi_google_oboe
        oboe

        # Links the log library to the target library.
        ${log-lib}
)